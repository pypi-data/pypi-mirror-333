from concurrent.futures import Future


class Response:
    def __init__(self, content, metadata):
        self.content = content
        self.metadata = metadata

    def __str__(self) -> str:
        return self.content.__str__()


class Stream:
    def __init__(self):
        pass

    def __iter__(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

class Llm:
    def __init__(self):
        pass

    def generate_text(self, system_prompt : str, prompt : str, max_tokens=None, temperature=None) -> Future[Stream | Response] :
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_config(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

