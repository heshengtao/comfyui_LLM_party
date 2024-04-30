class string_logic:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "option": (["A contain B","A not contain B","A equal B","A not equal B","A is null","A is not null"], {
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
    
    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("if","else",)

    FUNCTION = "str_logic"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具和函数（persona&function）"



    def str_logic(self,option,stringA=None,stringB=None):
        if option=="A contain B":
            out=stringA.find(stringB)>=0
        elif option=="A not contain B":
            out=stringA.find(stringB)==-1
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
        else:
            outif=""
            outelse=stringA
        return (outif,outelse,)