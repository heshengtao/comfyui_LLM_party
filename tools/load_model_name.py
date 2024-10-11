from ..config import config_keys, load_api_keys,config_path
import openai
api_keys = load_api_keys(config_path)

class load_name:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (config_keys, {"default": "your_model_name"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_name",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def file(self, model_name):
        out = model_name
        return (out,)
