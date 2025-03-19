import os

from ext_llm import Llm
import groq
from ext_llm.llm.llm import Stream, Response

class GroqLlm(Llm):

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        groq_api_key_env_var_name = config['groq_api_key_variable_name']
        groq_api_key = os.getenv(groq_api_key_env_var_name)
        if groq_api_key is None:
            raise ValueError(f"Environment variable {groq_api_key_env_var_name} not set")
        self.__groq_client = groq.Client(api_key=groq_api_key)

    def __invoke_model(self, system_prompt, prompt, max_tokens: int, temperature: float, top_p=0.9) -> Response | Stream:
        is_stream = self.config['invocation_method'] == 'converse_stream'
        chat_completion = self.__groq_client.chat.completions.create(
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model = self.config['model_id'],
            max_completion_tokens = max_tokens,
            temperature = temperature,
            top_p = top_p,
            stop=None,
            stream=is_stream
        )
        if is_stream:
            return GroqStream(chat_completion)
        else:
            return Response(chat_completion.choices[0].message.content, chat_completion)

    def generate_text(self, system_prompt : str, prompt : str, max_tokens=None, temperature=None) -> Stream | Response:
        if max_tokens is None:
            max_tokens = self.config['max_tokens']

        if temperature is None:
            temperature = self.config['temperature']

        if self.config['invocation_method'] != 'converse' and self.config['invocation_method'] != 'converse_stream':
            raise ValueError("Invalid invocation_method in config")
        return self.__invoke_model(system_prompt, prompt, max_tokens, temperature)

    def get_config(self):
        return self.config

class GroqStream(Stream):

    def __init__(self, stream):
        super().__init__()
        self.stream = stream

    def __iter__(self):
        for event in self.stream:
            yield Response(event.choices[0].delta, None)