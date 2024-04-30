import re


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

    CATEGORY = "大模型派对（llm_party）/函数（function）"



    def condition(self,text,is_enable="enable"):
        if is_enable=="disable":
            return (None,)
        # 使用正则表达式分割字符串
        parts = re.split(r'\*\*[0-9]:\*\* ', text)

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
        return (response1,response2,response3,)