
class Subject:
    def __init__(self):
        # 记录该通知的对象
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


# 模型的订阅者，用来获取模型的流式输出，并返回给observer
class ModelSubject(Subject):
    def __init__(self):
        super().__init__()
        # 记录当前所有的流式输出
        self.stream_token = []

        # 记录当前新的token
        self.new_token = ""

    def token_on_next(self, token):
        self.stream_token.append(token)
        self.new_token = token
        self.notify()

    def get_stream_token(self):
        return self.stream_token

    def get_new_token(self):
        return self.new_token
