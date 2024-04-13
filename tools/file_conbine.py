class file_conbine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
            "optional": {
                "file1": ("STRING", {
                    "forceInput": True
                }),
                "file2": ("STRING", {
                    "forceInput": True
                }),
                "file3": ("STRING", {
                    "forceInput": True
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("files",)

    FUNCTION = "conbine"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def conbine(self,file1=None,file2=None,file3=None):
        output=""
        file_all=[file1,file2,file3]
        for file in file_all:
            if file is not None:
                output+=file+"\n"
        return (output,)
    
class file_conbine_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
            "optional": {
                "file1": ("STRING", {
                    "forceInput": True
                }),
                "file2": ("STRING", {
                    "forceInput": True
                }),
                "file3": ("STRING", {
                    "forceInput": True
                }),
                "file4": ("STRING", {
                    "forceInput": True
                }),
                "file5": ("STRING", {
                    "forceInput": True
                }),
                "file6": ("STRING", {
                    "forceInput": True
                }),
                "file7": ("STRING", {
                    "forceInput": True
                }),
                "file8": ("STRING", {
                    "forceInput": True
                }),
                "file9": ("STRING", {
                    "forceInput": True
                }),
                "file10": ("STRING", {
                    "forceInput": True
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("files",)

    FUNCTION = "conbine"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def conbine(self,file1=None,file2=None,file3=None,file4=None,file5=None,file6=None,file7=None,file8=None,file9=None,file10=None):
        output=""
        file_all=[file1,file2,file3,file4,file5,file6,file7,file8,file9,file10]
        for file in file_all:
            if file is not None:
                output+=file+"\n"
        return (output,)