import ext_llm as xllm
import concurrent.futures
#read config yaml file
config : str = open("config.yaml").read()
#initialize extllm library


extllm = xllm.init(config)

llm_client = extllm.get_model("groq-llama")
llm_streaming_client = extllm.get_model("groq-llama-streaming")
custom_client = extllm.get_model("custom-provider")
#non blocking calls

print("first call")
future1 = llm_client.generate_text("Sei un assistente", "Recitami il primo articolo della costituzione italiana")
print("second call")
future2 = llm_streaming_client.generate_text("Sei un assistente", "Recitami il primo emendamento della costituzione americana")
# non blocking calls

print("third call on user implemented llm client class")
future3 = custom_client.generate_text("Sei un assistente", "Recitami il primo emendamento della costituzione americana")
print("-------------------waiting for third result------------------")
print(future3.result())

print("-------------------waiting for first result-------------------")
print(future1.result())
print("-------------------waiting for second result------------------")
stream = future2.result()
for event in stream:
    print(event)