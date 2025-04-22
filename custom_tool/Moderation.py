import locale
import os
import openai
from openai import OpenAI,AzureOpenAI
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
def check_text_legality(text):
    try:
        client = OpenAI(api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            client = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        # 调用审查模型
        response = client.moderations.create(
            input=text,
        )

        # 获取审查结果
        result = response.results[0]
        flagged_categories = []

        # 分析结果
        if result.flagged:
            # 遍历所有可能的属性并检查哪些为True
            category_attributes = [
                'harassment', 'harassment_threatening', 'hate', 'hate_threatening', 
                'self_harm', 'self_harm_instructions', 'self_harm_intent', 'sexual', 
                'sexual_minors', 'violence', 'violence_graphic', 'self-harm', 
                'sexual/minors', 'hate/threatening', 'violence/graphic', 
                'self-harm/intent', 'self-harm/instructions', 'harassment/threatening'
            ]
            
            for attr in category_attributes:
                # 使用 getattr() 提供默认值 False
                if getattr(result.categories, attr, False):
                    flagged_categories.append(attr)
                    
            return True, flagged_categories
        else:
            return False, "no flagged categories"
    except Exception as e:
        print(f"An error occurred: {e}")


class check_text():
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "text": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
            },
        }

    RETURN_TYPES = ("BOOLEAN","STRING","STRING",)
    RETURN_NAMES = ("flag","flagged_categories","text",)

    FUNCTION = "check"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def check(self, is_enable=True, text="", base_url=None, api_key=None):
        if is_enable == False:
            return (None,)
        if api_key != "":
            openai.api_key = api_key
        elif config.get("API_KEYS", "openai_api_key") != "":
            openai.api_key = config.get("API_KEYS", "openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            # 如果以/结尾
            if base_url[-1] == "/":
                openai.base_url = base_url
            else:
                openai.base_url = base_url + "/"
        elif config.get("API_KEYS", "base_url") != "":
            openai.base_url = config.get("API_KEYS", "base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        flag,flagged_categories = check_text_legality(text)
        if flag == False:
            return (flag,flagged_categories,text,)
        else:
            text=f"消息违规！违规范围：{flagged_categories}"
            return (flag,f"{flagged_categories}",text,)
        
NODE_CLASS_MAPPINGS = {
    "check_text": check_text,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"check_text": "☁️审核文本"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"check_text": "☁️moderation text"}