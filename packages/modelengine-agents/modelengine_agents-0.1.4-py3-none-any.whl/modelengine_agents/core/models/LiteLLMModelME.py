from typing import List, Optional, Dict

from modelengine_agents.agent_en import Tool
from modelengine_agents.agent_en.models import LiteLLMModel, ChatMessage, parse_tool_args_if_needed
from modelengine_agents.core.observer.subject import ModelSubject


class LiteLLMModelME(LiteLLMModel):
    def __init__(self, observer, *args, **kwargs):
        self.subject = ModelSubject()
        self.subject.attach(observer)
        super().__init__(*args, **kwargs)

    # 支持流式输出
    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        try:
            import litellm
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install 'litellm' extra to use LiteLLMModel: `pip install litellm'`"
            )

        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            model=self.model_id,
            api_base=self.api_base,
            api_key=self.api_key,
            convert_images_to_image_urls=True,
            flatten_messages_as_text=self.flatten_messages_as_text,
            custom_role_conversions=self.custom_role_conversions,
            stream=True,
            **kwargs,
        )
        # stream=True 流式输出
        stream_response = litellm.completion(**completion_kwargs)
        chunks = []
        for chunk in stream_response:
            new_token = chunk['choices'][0]['delta']['content']
            if new_token is not None:
                print(new_token, end='')
                self.subject.token_on_next(new_token)
            chunks.append(chunk)
        self.subject.token_on_next("\n")

        response = litellm.stream_chunk_builder(chunks, messages=messages)

        # 统计花费的token数
        self.last_input_token_count = response.usage.prompt_tokens
        self.last_output_token_count = response.usage.completion_tokens
        message = ChatMessage.from_dict(
            response.choices[0].message.model_dump(include={"role", "content", "tool_calls"})
        )

        message.raw = response

        if tools_to_call_from is not None:
            return parse_tool_args_if_needed(message)
        return message