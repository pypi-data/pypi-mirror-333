import concurrent.futures
from concurrent.futures import Future

from ext_llm import Llm
from ext_llm.llm.llm import Stream, Response


class LlmConcurrencyProxy(Llm):

    def __init__(self, llm: Llm):
        super().__init__()
        self.llm = llm
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def generate_text(self, system_prompt: str, prompt: str, max_tokens=None, temperature=None) -> Future[Stream | Response]:
        future = self.executor.submit(self.llm.generate_text, system_prompt, prompt, max_tokens, temperature)
        return future

    def get_config(self):
        return self.llm.get_config()