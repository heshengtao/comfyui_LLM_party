class load_int:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("INT", {"default": 0}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)

    FUNCTION = "tts"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def tts(self, text):
        text = int(text)
        return (text,)
