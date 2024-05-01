import re


class string_logic:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "option": (["A contain B","A not contain B","A relate to B","A not relate to B","A equal B","A not equal B","A is null","A is not null"], {
                    "default": "A contain B",
                })
            },
            "optional": {
                "stringA": ("STRING", {
                }),
                "stringB": ("STRING", {
                }),
            }
        }
    
    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("if","else","is_true",)

    FUNCTION = "str_logic"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/函数（function）"



    def str_logic(self,option,stringA=None,stringB=None):
        if option=="A contain B":
            out=stringA.find(stringB)>=0
        elif option=="A not contain B":
            out=stringA.find(stringB)==-1
        elif option == "A relate to B":
            # A relate to B means A contains any part of B after splitting by comma or semicolon
            parts = re.split(r'[，,、]', stringB)
            out = any(part in stringA for part in parts)
        elif option == "A not relate to B":
            # A not relate to B means A does not contain any part of B after splitting by comma or semicolon
            parts = re.split(r'[，,、]', stringB)
            out = not any(part in stringA for part in parts)
        elif option=="A equal B":
            out=stringA==stringB
        elif option=="A not equal B":
            out=stringA!=stringB
        elif option=="A is null":
            out=stringA==None
        elif option=="A is not null":
            out=stringA!=None

        if out:
            outif=stringA
            outelse=""
            out="enable"
        else:
            outif=""
            outelse=stringA
            out="disable"
        return (outif,outelse,out)