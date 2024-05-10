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

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def condition(self, text, is_enable=True):
        if is_enable == False:
            return (None,)
        # 使用正则表达式分割字符串
        parts = re.split(r"\*\*[0-9]:\*\* ", text)

        # 移除列表中的空字符串
        parts = [part for part in parts if part]

        # 根据分割后的部分数量，赋值给response变量
        response1, response2, response3 = (parts + ["", "", ""])[:3]
        if response1.strip() == "" or response1.strip() == "empty":
            response1 = None
        if response2.strip() == "" or response2.strip() == "empty":
            response2 = None
        if response3.strip() == "" or response3.strip() == "empty":
            response3 = None
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

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def condition(self, text, is_enable=True):
        if is_enable == False:
            return (None,)
        # 使用正则表达式分割字符串
        parts = re.split(r"\*\*[0-9]+:\*\* ", text)

        # 移除列表中的空字符串
        parts = [part for part in parts if part]

        # 根据分割后的部分数量，赋值给response变量
        (
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
        ) = (parts + ["", "", ""])[:10]
        if response1.strip() == "" or response1.strip() == "empty":
            response1 = None
        if response2.strip() == "" or response2.strip() == "empty":
            response2 = None
        if response3.strip() == "" or response3.strip() == "empty":
            response3 = None
        if response4.strip() == "" or response4.strip() == "empty":
            response4 = None
        if response5.strip() == "" or response5.strip() == "empty":
            response5 = None
        if response6.strip() == "" or response6.strip() == "empty":
            response6 = None
        if response7.strip() == "" or response7.strip() == "empty":
            response7 = None
        if response8.strip() == "" or response8.strip() == "empty":
            response8 = None
        if response9.strip() == "" or response9.strip() == "empty":
            response9 = None
        if response10.strip() == "" or response10.strip() == "empty":
            response10 = None
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
