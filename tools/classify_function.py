import json
import re


class classify_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "text": ("STRING", {"forceInput": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "response1",
        "response2",
        "response3",
    )

    FUNCTION = "condition"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def condition(self, text, is_enable=True):
        if is_enable == False:
            return (None,)
        # text转成字典
        text=json.loads(text)
        response1 = text.get('1')
        response2 = text.get('2')
        response3 = text.get('3')
        return (
            response1,
            response2,
            response3,
        )


class classify_function_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "text": ("STRING", {"forceInput": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "response1",
        "response2",
        "response3",
        "response4",
        "response5",
        "response6",
        "response7",
        "response8",
        "response9",
        "response10",
    )

    FUNCTION = "condition"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def condition(self, text, is_enable=True):
        if is_enable == False:
            return (None,)
        text=json.loads(text)
        response1 = text.get('1')
        response2 = text.get('2')
        response3 = text.get('3')
        response4 = text.get('4')
        response5 = text.get('5')
        response6 = text.get('6')
        response7 = text.get('7')
        response8 = text.get('8')
        response9 = text.get('9')
        response10 = text.get('10')
        return (
            response1,
            response2,
            response3,
            response4,
            response5,
            response6,
            response7,
            response8,
            response9,
            response10,
        )
