class translate_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "language_A": ("STRING", {"default": "中文"}),
                "language_B": ("STRING", {"default": "英文"}),
            },
            "optional": {
                "tone": ("STRING", {"default": "正式"}),
                "degree": ("INT", {"default": 5, " min": 0, "max": 10}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt_input",)

    FUNCTION = "condition"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def condition(self, language_A, language_B, degree=5, tone="正式", is_enable=True):
        if is_enable == False:
            return (None,)
        sys_prompt = f"""你是一个翻译专家，请将我的输入从{language_A}翻译成{language_B}，语气为{tone}，语气程度为{str(degree)}。
语气程度最大为10，最小为0，数字越大语气越{tone}。当语气程度为0时，几乎不改变原文的语气，当语气程度为10时，语气会非常{tone}。
如果 {language_A}和{language_B}相同，也请注意语气的调整，而不是返回原内容。
翻译时不要复述原文以及其他无关内容，直接返回翻译后的内容即可。注意！如果我输入的内容带有格式（例如markdown格式），请保留原格式。

如果是markdown格式的文字，有以下要求：
1. 请保留原格式，不要改变markdown格式。
2. 请不要改变markdown格式中的超链接中的()部分，但[]中的内容必须翻译。如果改变了()部分，可能会导致超链接失效。
3. HTML格式的文字，请保留原格式，不要改变HTML格式,其中会被显示在前端的文字需要翻译，而链接部分不能翻译。

从现在开始，请将以下内容翻译成{language_B}。
        """
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)
