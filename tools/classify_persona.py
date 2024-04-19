

class classify_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                })
            },
            "optional": {
                "text1": ("STRING", {

                }),
                "text2": ("STRING", {

                }),
                "text3": ("STRING", {

                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt",)

    FUNCTION = "condition"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def condition(self,text1=None,text2=None,text3=None,is_enable="enable"):
        if is_enable=="disable":
            return (None,)
        sys_prompt=f"""
            # 文本分类助理
            你是一个文本分类助理。
            ## 任务
            我将给你需要分类的文本，你需要帮我按照下文给出的分类原则进行分类，并按照严格下文给出的格式回复我。
            ##分类原则
            1. 如果文本中包含"{text1}"或者与"{text1}"有关或者满足"{text1}"中提及的条件的文本，则将其分类为第一类。
            2. 如果文本中包含"{text2}"或者与"{text2}"有关或者满足"{text2}"中提及的条件的文本，则将其分类为第二类。
            3. 如果文本中包含"{text3}"或者与"{text3}"有关或者满足"{text3}"中提及的条件的文本，则将其分类为第三类。
            4. 如果以上某一个或若干个分类条件为【如果文本中包含""或者与""有关，则将其分类为...】,则不要将任何文本分到这一类或这些类中,因为空字符串与任何文本无关。
            ## 回复格式
            以字符串的形式回复，并严格按照下文给出的格式回复我。
            你每一类的输出以“**1:**”开头。以下是一个完整的输出示例：
            **1:** 分到第一类的文本
            **2:** 分到第二类的文本
            **3:** 分到第三类的文本
            ## 限制
            1. 输出时不要包含任何多余的文本，只输出分类结果。
            2. 不要在输出中包含任何多余的空格。

            以下为需要分类的文本：
        """
        sys_prompt=sys_prompt.strip()
        return (sys_prompt,)