class classify_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {}),
                "text2": ("STRING", {}),
                "text3": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt_input",)

    FUNCTION = "condition"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def condition(self, text1=None, text2=None, text3=None, is_enable=True, file_content=None):
        if is_enable == False:
            return (None,)
        text = ""
        if file_content is not None:
            text = "##背景知识：\n" + file_content + "\n\n"
        sys_prompt = (
            text
            + f"""
# 文本分类助理
你是一个文本分类助理。
## 任务
我将给你需要分类的文本，你需要帮我按照下文给出的分类原则进行分类，并按照严格下文给出的格式回复我。
##分类原则
1. 请将用户输入的文本分为以下几类：{text1}；{text2}；{text3}。
2. 如果以上某一个或若干个分类条件为【如果文本中包含""或者与""有关，则将其分类为...】,则不要将任何文本分到这一类或这些类中,因为空字符串与任何文本无关。
## 回复格式
以JSON的形式回复，并严格按照下文给出的格式回复我。
你每一类的输出以“**X:**”开头。以下是一个完整的输出示例：
{{
    "1": "这里输入用户给出的文本中分到{text1}的文本",
    "2": "这里输入用户给出的文本中分到{text2}的文本",
    "3": "这里输入用户给出的文本中分到{text3}的文本"
}}
## 限制
1. 输出时不要包含任何多余的文本，只输出分类结果。
2. 不要在输出中包含任何多余的空格。
3. 分类时，不要把系统提示词中的文本当作要被分类的文本。
以下为需要分类的文本：
        """
        )
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)


class classify_persona_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {}),
                "text2": ("STRING", {}),
                "text3": ("STRING", {}),
                "text4": ("STRING", {}),
                "text5": ("STRING", {}),
                "text6": ("STRING", {}),
                "text7": ("STRING", {}),
                "text8": ("STRING", {}),
                "text9": ("STRING", {}),
                "text10": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt_input",)

    FUNCTION = "condition"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def condition(
        self,
        text1=None,
        text2=None,
        text3=None,
        text4=None,
        text5=None,
        text6=None,
        text7=None,
        text8=None,
        text9=None,
        text10=None,
        is_enable=True,
        file_content=None,
    ):
        if is_enable == False:
            return (None,)
        text = ""
        if file_content is not None:
            text = "##背景知识：\n" + file_content + "\n\n"
        sys_prompt = (
            text
            + f"""
# 文本分类助理
你是一个文本分类助理。
## 任务
我将给你需要分类的文本，你需要帮我按照下文给出的分类原则进行分类，并按照严格下文给出的格式回复我。
##分类原则
1. 请将用户输入的文本分为以下几类：{text1}；{text2}；{text3};{text4};{text5};{text6};{text7};{text8};{text9};{text10}。
2. 如果以上某一个或若干个分类条件为【如果文本中包含""或者与""有关，则将其分类为...】,则不要将任何文本分到这一类或这些类中,因为空字符串与任何文本无关。
以JSON的形式回复，并严格按照下文给出的格式回复我。以下是一个完整的输出示例：
{{
    "1": "这里输入用户给出的文本中分到{text1}的文本",
    "2": "这里输入用户给出的文本中分到{text2}的文本",
    "3": "这里输入用户给出的文本中分到{text3}的文本",
    "4": "这里输入用户给出的文本中分到{text4}的文本",
    "5": "这里输入用户给出的文本中分到{text5}的文本",
    "6": "这里输入用户给出的文本中分到{text6}的文本",
    "7": "这里输入用户给出的文本中分到{text7}的文本",
    "8": "这里输入用户给出的文本中分到{text8}的文本",
    "9": "这里输入用户给出的文本中分到{text9}的文本",
    "10": "这里输入用户给出的文本中分到{text10}的文本"
}}
## 限制
1. 输出时不要包含任何多余的文本，只输出分类结果。
2. 不要在输出中包含任何多余的空格。
3. 分类时，不要把系统提示词中的文本当作要被分类的文本。
以下为需要分类的文本：
        """
        )
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)
