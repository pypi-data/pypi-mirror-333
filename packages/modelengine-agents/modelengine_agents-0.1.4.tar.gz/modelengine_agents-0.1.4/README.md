# app-engine


# ModelEngine Agents Core

ModelEngine Agents Core 是一个基于 SmoLAgent 的增强版本,提供了丰富的 Agent 工具集和流式输出能力。

## 主要特性

- 继承 SmoLAgent 的核心能力
- 支持多种 Agent 工具:
  - Baidu 搜索/ Google 搜索
  - 格式化输出工具
- 流式输出支持
- 基于 FastAPI 的服务端实现
- 可扩展的消息观察者模式

## 核心组件

### CodeAgentME
代码执行 Agent,支持 Python 代码的解释和执行。

### LiteLLMModelME & OpenAIServerModelME 
支持多种 LLM 模型的接入。

### 工具集
- BaiduSearchTool: 百度搜索工具，通过爬虫实现检索，无需API。
- GoogleSearchTool: Google搜索工具，通过爬虫实现检索，无需API。
- EXASearchTool: EXA搜索工具，需要提供API-KEY。
- DuckDuckGoSearchTool: SmolAgent内置搜索工具，用多了会有速率限制。
- FinalAnswerFormatTool: 输出格式化工具，支持传入prompt控制输出格式。

### MessageObserver
消息观察者模式实现,用于处理 Agent 的流式输出。

## 使用方式
参考modelengine_agents.core server.py



