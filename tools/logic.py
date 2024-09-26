import re


class string_logic:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "option": (
                    [
                        "A contain B",
                        "A not contain B",
                        "A relate to B",
                        "A not relate to B",
                        "A equal B",
                        "A not equal B",
                        "A is null",
                        "A is not null",
                    ],
                    {
                        "default": "A contain B",
                    },
                )
            },
            "optional": {
                "stringA": ("STRING", {}),
                "stringB": ("STRING", {}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "BOOLEAN",
        "BOOLEAN",
    )
    RETURN_NAMES = (
        "if",
        "else",
        "is_true",
        "is_false",
    )

    FUNCTION = "str_logic"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def str_logic(self, option, stringA="", stringB=""):
        if stringA is None or stringA == "":
            return (
                None,
                None,
                False,
                True,
            )

        if option == "A contain B":
            out = stringA.find(stringB) >= 0
        elif option == "A not contain B":
            out = stringA.find(stringB) == -1
        elif option == "A relate to B":
            # A relate to B means A contains any part of B after splitting by comma or semicolon
            parts = re.split(r"[，,、]", stringB)
            out = any(part in stringA for part in parts)
        elif option == "A not relate to B":
            # A not relate to B means A does not contain any part of B after splitting by comma or semicolon
            parts = re.split(r"[，,、]", stringB)
            out = not any(part in stringA for part in parts)
        elif option == "A equal B":
            out = stringA == stringB
        elif option == "A not equal B":
            out = stringA != stringB
        elif option == "A is null":
            out = stringA == None
        elif option == "A is not null":
            out = stringA != None

        if out:
            outif = stringA
            outelse = ""
            out = True
            out2 = False
        else:
            outif = ""
            outelse = stringA
            out = False
            out2 = True
        return (
            outif,
            outelse,
            out,
            out2,
        )


import re


class substring:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"multiline": True}),
            },
            "optional": {
                "start_string": ("STRING", {}),
                "end_string": ("STRING", {}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "substring",
        "remaining_string",
    )

    FUNCTION = "substr"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def substr(self, input_string, start_string="", end_string=""):
        if input_string == "" or input_string is None:
            return (None, None)
        if start_string == "" and end_string == "":
            out = input_string
            remaining_string = ""
        elif start_string == "":
            end_index = input_string.find(end_string)
            out = input_string[:end_index]
            remaining_string = input_string[end_index + len(end_string) :]
        elif end_string == "":
            start_index = input_string.find(start_string) + len(start_string)
            out = input_string[start_index:]
            remaining_string = input_string[: start_index - len(start_string)]
        else:
            start_index = input_string.find(start_string) + len(start_string)
            end_index = input_string.find(end_string, start_index)
            out = input_string[start_index:end_index]
            remaining_string = (
                input_string[: start_index - len(start_string)] + input_string[end_index + len(end_string) :]
            )

        out = out.strip()
        remaining_string = remaining_string.strip()
        return (out, remaining_string,)


class get_string:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)

    FUNCTION = "substr"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def substr(self, input_string):
        out = input_string
        return (out,)


class replace_string:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {}),
                "old_string": ("STRING", {"default": ""}),
                "new_string": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)

    FUNCTION = "substr"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def substr(self, old_string, new_string, input_string=""):
        out = input_string.replace(old_string, new_string)
        return (out,)
