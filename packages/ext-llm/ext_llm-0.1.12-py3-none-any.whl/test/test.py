import ext_llm
import concurrent.futures
#read config yaml file
config : str = open("config.yaml").read()
#initialize extllm library


extllm = ext_llm.init(config)

llm_client = extllm.get_client("groq-llama")
llm_concurrent_client = extllm.get_concurrent_client("groq-llama")
#non blocking calls

print("first call (non-blocking)")
future1 = llm_concurrent_client.generate_text("Sei un assistente", "Recitami il primo articolo della costituzione italiana")
print("second call (blocking)")
print("While waiting for this blocking call to finish, the first call should be completed ...")
result = llm_client.generate_text("Sei un assistente", "Recitami il primo emendamento della costituzione americana")
print("----- result -----")
print(result.metadata)
print(result)
print("----- future 1 -----")
print(future1.result().metadata)
print(future1.result())
