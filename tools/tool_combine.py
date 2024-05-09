import json


def remove_duplicates(dicts):
    name_to_dict = {}
    for d in dicts:
        if "function" in d and "name" in d["function"]:
            function_name = d["function"]["name"]
            name_to_dict[function_name] = d

    return list(name_to_dict.values())


class tool_combine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "tool1": ("STRING", {"forceInput": True}),
                "tool2": ("STRING", {"forceInput": True}),
                "tool3": ("STRING", {"forceInput": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(self, is_enable=True, tool1=None, tool2=None, tool3=None):
        if is_enable == False:
            return (None,)
        output = []
        tool_all = [tool1, tool2, tool3]
        for tool in tool_all:
            if tool is not None:
                tool = json.loads(tool)
                output.extend(tool)
        if output != []:
            output = remove_duplicates(output)
            out = json.dumps(output, ensure_ascii=False)
        else:
            out = None
        return (out,)


class tool_combine_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "tool1": ("STRING", {"forceInput": True}),
                "tool2": ("STRING", {"forceInput": True}),
                "tool3": ("STRING", {"forceInput": True}),
                "tool4": ("STRING", {"forceInput": True}),
                "tool5": ("STRING", {"forceInput": True}),
                "tool6": ("STRING", {"forceInput": True}),
                "tool7": ("STRING", {"forceInput": True}),
                "tool8": ("STRING", {"forceInput": True}),
                "tool9": ("STRING", {"forceInput": True}),
                "tool10": ("STRING", {"forceInput": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(
        self,
        is_enable=True,
        tool1=None,
        tool2=None,
        tool3=None,
        tool4=None,
        tool5=None,
        tool6=None,
        tool7=None,
        tool8=None,
        tool9=None,
        tool10=None,
    ):
        if is_enable == False:
            return (None,)
        output = []
        tool_all = [tool1, tool2, tool3, tool4, tool5, tool6, tool7, tool8, tool9, tool10]
        for tool in tool_all:
            if tool:
                try:
                    tool = json.loads(tool)
                    output.extend(tool)
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
        if output != []:
            output = remove_duplicates(output)
            out = json.dumps(output, ensure_ascii=False)
        else:
            out = None
        return (out,)
