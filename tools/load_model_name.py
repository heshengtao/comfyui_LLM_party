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

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, model_name):
        out = model_name
        return (out,)
    
api_key=api_keys.get("openai_api_key").strip()
base_url=api_keys.get("base_url").strip()
if api_key == "" or api_key =="sk-XXXXX" or base_url == "":
    models_dict =[]
else:
    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        models_response = client.models.list()
        # 将模型列表转换为字典
        models_dict = [model.id for model in models_response.data]
    except Exception as e:
        models_dict = []
class load_name_v2:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (models_dict, {"default": "gpt-4o-mini"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_name",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, model_name):
        out = model_name
        return (out,)