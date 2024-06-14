from ..config import config_keys


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
        out=model_name
        return (out,)

