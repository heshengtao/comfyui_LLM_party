class show_text_party:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def notify(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]:
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [text]

        return {"ui": {"text": text}, "result": (text,)}


class About_us:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "大模型派对（llm_party）"

    def notify(self, unique_id=None, extra_pnginfo=None):
        text = [
            f"""
This is an easter egg node of the project.
comfyui_LLM_party
Project Initiator: heshengtao
Project URL: https://github.com/heshengtao/comfyui_LLM_party
Project Media Channel: https://space.bilibili.com/26978344?spm_id_from=333.1007.0.0
Special thanks to the following project contributors:
1. [bigcat88](https://github.com/bigcat88)
2. [guobalove](https://github.com/guobalove)
        """.strip()
        ]
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]:
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    # 直接赋值，不进行转换
                    node["widgets_values"] = [text]
        return {"ui": {"text": text}, "result": (text,)}
