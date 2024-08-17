import json


class custom_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "根据背景知识，请帮我写一篇关于/{主题/}的文章。",
                    },
                ),
                "prompt_template": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": '{"主题":"人工智能"}',
                    },
                ),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt",)

    FUNCTION = "custom"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def custom(self, prompt, prompt_template, is_enable=True, file_content=None):
        if is_enable == False:
            return (None,)
        text = ""
        if file_content is not None:
            text = "##背景知识：\n" + file_content + "\n\n"
        sys_prompt = (
            text
            + f"""
            请依次执行以下步骤：
            1. 请根据{prompt_template}中的规则，替换{prompt}中的变量，生成一段符合规则的文本。
            2. 请将第一步生成的文本中的{{text}}变量替换为用户输入的文本，如果没有则不用替换，跳过这一步。
            3. 回复第二步生成的文本,回复时不用告诉用户你的思考过程，直接对第二步生成的文本进行回复即可。
            下面为用户输入的文本：
        """
        )
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)
