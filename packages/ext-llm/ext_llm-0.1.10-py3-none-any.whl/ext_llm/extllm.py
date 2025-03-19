from ext_llm import ExtLlmContext, Llm
from ext_llm.llm.concurrency_proxy import LlmConcurrencyProxy
from ext_llm.llm.logging_proxy import LlmLoggingProxy

class ExtLlm:

    provider_dict = {
        "groq" : ["ext_llm.llm.groq_llm", "GroqLlm"],
        "aws" : ["ext_llm.llm.aws_llm", "AwsLlm"]
    }

    def __init__(self, context: ExtLlmContext):
        self.context = context

    def list_available_models(self):
        return self.context.get_configs()["presets"]

    def get_model(self, preset_name: str, module_name="ext_llm.llm") -> Llm:
        class_name = None
        module_name = None
        if preset_name not in self.context.get_configs()["presets"]:
            raise Exception("Preset not found")

        if "provider" in self.context.get_configs()["presets"][preset_name]:
            class_name = self.provider_dict[self.context.get_configs()["presets"][preset_name]["provider"]][1]
            module_name = self.provider_dict[self.context.get_configs()["presets"][preset_name]["provider"]][0]
        else:
            class_name = self.context.get_configs()["presets"][preset_name]["class_name"]
            module_name=self.context.get_configs()["presets"][preset_name]["module_name"]

        try:
            module = __import__(module_name, fromlist=[class_name])
        except KeyError:
            module = __import__(module_name, fromlist=[class_name])
        if hasattr(module, class_name):
            return LlmConcurrencyProxy(LlmLoggingProxy(getattr(module, class_name)(self.context.get_configs()["presets"][preset_name])))
        else:
            raise Exception("Class not found")
