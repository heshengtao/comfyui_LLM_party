import locale
import os
from peft import PeftModel
import torch

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lora_dir = os.path.join(current_dir, "model", "LORA")

# 获取 lora_path 中的所有文件夹列表
lora_list = [f for f in os.listdir(lora_dir) if os.path.isdir(os.path.join(lora_dir, f))]

def merge_lora_weights(model, lora_path):
    # 加载 LoRA 权重
    model = PeftModel.from_pretrained(model, lora_path)
    return model

class load_llm_lora:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "model": ("CUSTOM", {}),
                "lora_path": ("STRING", {"default": "", "description": "Path to the LoRA folder."}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)

    FUNCTION = "apply_lora"  # 将 FUNCTION 指向实际的方法名

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def apply_lora(self, model, lora_path, is_enable=True):
        # 合并 LoRA 权重
        model = merge_lora_weights(model, lora_path)
        
        if is_enable:
            model.enable_adapter_layers()  # 启用 LoRA 层
        else:
            model.disable_adapter_layers()  # 禁用 LoRA 层
        
        return (model,)

        
class easy_load_llm_lora:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default":True}),
                "model": ("CUSTOM", {}),
                "lora_path": (lora_list, {"default": ""}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)

    FUNCTION = "sleep"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def sleep(self,model,lora_path,is_enable=True):
        lora_path=os.path.join(lora_dir,lora_path)
        model=merge_lora_weights(model, lora_path)
        if is_enable:
            model.enable_adapter_layers()  # 启用 LoRA 层
        else:
            model.disable_adapter_layers()  # 禁用 LoRA 层

        return (model,)
    
NODE_CLASS_MAPPINGS = {"load_llm_lora": load_llm_lora, "easy_load_llm_lora": easy_load_llm_lora}
# 获取系统语言
lang = locale.getdefaultlocale()[0]
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
    NODE_DISPLAY_NAME_MAPPINGS = {"load_llm_lora": "加载LLM LoRA", "easy_load_llm_lora": "简易加载LLM LoRA"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"load_llm_lora": "Load LLM LoRA", "easy_load_llm_lora": "Easy Load LLM LoRA"}