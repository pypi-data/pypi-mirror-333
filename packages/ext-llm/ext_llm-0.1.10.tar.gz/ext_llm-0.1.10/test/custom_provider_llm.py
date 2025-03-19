from ext_llm import Llm


class MyLlm(Llm):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def generate_text(self, system_prompt: str, prompt: str, max_tokens=None, temperature=None):
        return "Hello, world!"