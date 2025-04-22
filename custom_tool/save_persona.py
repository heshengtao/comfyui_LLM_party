# 当前脚本目录的上级目录
import locale
import os


current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
persona_path = os.path.join(current_dir, "persona")

class savepersona:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "persona_name": ("STRING", {"default":"example"}),
            "text": ("STRING", {"forceInput": True})
            }}

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def save(self, persona_name,text):
        # 保存为persona_path下的example.txt文件
        with open(os.path.join(persona_path, persona_name + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
        return ()


NODE_CLASS_MAPPINGS = {"savepersona": savepersona}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"savepersona": "保存人格面具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"savepersona": "Save Persona"}