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


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


class none2false:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any": (any_type, {}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_not_none",)

    FUNCTION = "tts"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def tts(self, any):
        if any is None:
            return (False,)
        else:
            return (True,)


class bool_logic:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "A": ("BOOLEAN", {}),
                "logic_type": (["and", "or", "not", "Nor", "Nand", "Xor", "Xnor"], {"default": "and"}),
            },
            "optional": {
                "B": ("BOOLEAN", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)

    FUNCTION = "tts"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def tts(self, A, B=True, logic_type="and"):
        if logic_type == "and":
            return (A and B,)
        elif logic_type == "or":
            return (A or B,)
        elif logic_type == "not":
            return (not A,)
        elif logic_type == "Nor":
            return (not (A or B),)
        elif logic_type == "Nand":
            return (not (A and B),)
        elif logic_type == "Xor":
            return (A ^ B,)
        elif logic_type == "Xnor":
            return (not (A ^ B),)


class str2float:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)

    FUNCTION = "tts"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def tts(self, text):
        return (float(text),)