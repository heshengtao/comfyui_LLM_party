import json
import numpy as np
from transformers import AutoModel, AutoTokenizer
import locale
import numpy as np
from PIL import Image
import os
import torch
if torch.cuda.is_available():
    from transformers import BitsAndBytesConfig
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 在current_dir_path下创建一个名为output的文件夹
output_dir_path = os.path.join(current_dir_path, 'output')
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)
def perform_ocr(model_name_or_path, device, ocr_type, image_path,ocr_box, ocr_color, multi_crop,render,out_dir_path,dtype):
    model_kwargs = {
        'device_map': device,
    }    
    if dtype == "float16":
        model_kwargs['torch_dtype'] = torch.float16
    elif dtype == "bfloat16":
        model_kwargs['torch_dtype'] = torch.bfloat16
    elif dtype in ["int8", "int4"]:
        model_kwargs['quantization_config'] = BitsAndBytesConfig(load_in_8bit=(dtype == "int8"), load_in_4bit=(dtype == "int4"))
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True, low_cpu_mem_usage=True, use_safetensors=True, pad_token_id=tokenizer.eos_token_id,**model_kwargs)
    model = model.eval()
    if render:    
        html_path = os.path.join(out_dir_path, 'render.html')
        res = model.chat(tokenizer, image_path, ocr_type='format', render=True, save_render_file = html_path)
    elif multi_crop:
        res = model.chat_crop(tokenizer, image_path, ocr_type=ocr_type)
    else:
        res = model.chat(tokenizer, image_path, ocr_type=ocr_type, ocr_box=ocr_box, ocr_color=ocr_color)
    return res


class got_ocr:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name_or_path": ("STRING", {"default": ""}),
                "device": (["auto","cuda", "cpu", "mps"], {"default": "auto"}),
                "ocr_type": (["ocr","format"], {"default": "format"}),
                "image": ("IMAGE", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "ocr_box": ("STRING", {"default": ""}),
                "ocr_color": ("STRING", {"default": ""}),
                "multi_crop": ("BOOLEAN", {"default": False}),
                "render": ("BOOLEAN", {"default": False}),
                "out_dir_path": ("STRING", {"default": output_dir_path}),
                "dtype":(["float32", "float16","bfloat16", "int8", "int4"],{"default":"bfloat16"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/图片（image）"

    def time(self, model_name_or_path, device, ocr_type, image,ocr_box, ocr_color, multi_crop,dtype, is_enable=True,render=False,out_dir_path=output_dir_path):
        if is_enable == False:
            return (None,)
        # 保存image到本地output_dir_path 
        if image is not None and len(image) > 0:
            image = image[0]
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # 将图像转换为 RGB 模式并保存为 JPG 格式
            img = img.convert("RGB")
            img.save(os.path.join(output_dir_path, 'temp.png'))
            image_path = os.path.join(output_dir_path, 'temp.png')
            res=perform_ocr(model_name_or_path, device, ocr_type, image_path,ocr_box, ocr_color, multi_crop,render,out_dir_path,dtype)
            return (res,)
        else:
            return (None,)


NODE_CLASS_MAPPINGS = {"got_ocr": got_ocr}
# 获取系统语言
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
    NODE_DISPLAY_NAME_MAPPINGS = {"got_ocr": "🖥️GOT-OCR2"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"got_ocr": "🖥️GOT-OCR2"}