class translate_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "language_A":("STRING", {"default": "中文"}),
                "language_B":("STRING", {"default": "英文"}),
            },
            "optional": {
                "tone": ("STRING", {"default": "正式"}),
                "degree":("INT", {"default": 5," min": 0, "max": 10}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt",)

    FUNCTION = "condition"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def condition(self, language_A, language_B,degree=5, tone="正式", is_enable=True):
        if is_enable == False:
            return (None,)
        sys_prompt=f"""你是一个翻译专家，请将用户的输入从{language_A}翻译成{language_B}，语气为{tone}，语气程度为{str(degree)}。
语气程度最大为10，最小为0，数字越大语气越{tone}。当语气程度为0时，几乎不改变原文的语气，当语气程度为10时，语气会非常{tone}。
如果 {language_A}和{language_B}相同，也请注意语气的调整，而不是返回原内容。
翻译时不要复述原文以及其他无关内容，直接返回翻译后的内容即可。
从现在开始，请将以下内容翻译成{language_B}。
        """
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)