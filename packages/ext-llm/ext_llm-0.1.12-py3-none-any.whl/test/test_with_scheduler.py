import time

import ext_llm
import concurrent.futures

from ext_llm.scheduler import RequestScheduler

#read config yaml file
config : str = open("config.yaml").read()
#initialize extllm library
extllm = ext_llm.init(config)

llm_client = extllm.get_client("groq-llama")
scheduler = RequestScheduler(llm_client, max_workers=4, rate_limit_per_minute=10)
scheduler.start()

request_1 = scheduler.submit_request("you are a helpful assistant",
                                     "What is the capital of France?",)

request_2 = scheduler.submit_request("you are a helpful assistant",
                                        "What is the capital of Germany?",)

request_3 = scheduler.submit_request("you are a helpful assistant",
                                        "What is the capital of Italy?",)


print("Request 1:", scheduler.get_result(request_1))
print("Request 2:", scheduler.get_result(request_2))
print("Request 3:", scheduler.get_result(request_3))

scheduler.stop()