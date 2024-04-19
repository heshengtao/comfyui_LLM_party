class classify_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),
                "text": ("STRING", {
                    "forceInput": True
                }),
            },
            "optional": {

            }
        }
    
    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("response1","response2","response3",)

    FUNCTION = "condition"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def condition(self,text,is_enable="enable"):
        if is_enable=="disable":
            return (None,)
        # 定义一个安全的分割函数
        def safe_split(s, delimiter):
            return s.split(delimiter)[1] if delimiter in s else ''

        # 提取不同部分的文本
        response1 = safe_split(text, '**1:** ').split(' **2:**')[0]
        response2 = safe_split(text, '**2:** ').split(' **3:**')[0]
        response3 = safe_split(text, '**3:** ')

        return (response1,response2,response3,)