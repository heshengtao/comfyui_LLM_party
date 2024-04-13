import json


class tool_conbine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
            "optional": {
                "tool1": ("STRING", {
                    "forceInput": True
                }),
                "tool2": ("STRING", {
                    "forceInput": True
                }),
                "tool3": ("STRING", {
                    "forceInput": True
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "conbine"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def conbine(self,tool1=None,tool2=None,tool3=None):
        output=[]
        tool_all=[tool1,tool2,tool3]
        for tool in tool_all:
            if tool is not None:
                tool=json.loads(tool)
                output.extend(tool)
        if output!=[]:
            out=json.dumps(output, ensure_ascii=False)
        else:
            out=None
        return (out,)
    

class tool_conbine_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
            "optional": {
                "tool1": ("STRING", {
                    "forceInput": True
                }),
                "tool2": ("STRING", {
                    "forceInput": True
                }),
                "tool3": ("STRING", {
                    "forceInput": True
                }),
                "tool4": ("STRING", {
                    "forceInput": True
                }),
                "tool5": ("STRING", {
                    "forceInput": True
                }),
                "tool6": ("STRING", {
                    "forceInput": True
                }),
                "tool7": ("STRING", {
                    "forceInput": True
                }),
                "tool8": ("STRING", {
                    "forceInput": True
                }),
                "tool9": ("STRING", {
                    "forceInput": True
                }),
                "tool10": ("STRING", {
                    "forceInput": True
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "conbine"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def conbine(self,tool1=None,tool2=None,tool3=None,tool4=None,tool5=None,tool6=None,tool7=None,tool8=None,tool9=None,tool10=None):
        output=[]
        tool_all=[tool1,tool2,tool3,tool4,tool5,tool6,tool7,tool8,tool9,tool10]
        for tool in tool_all:
            if tool:
                try:
                    tool = json.loads(tool)
                    output.extend(tool)
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
        if output!=[]:
            out=json.dumps(output, ensure_ascii=False)
        else:
            out=None
        return (out,)