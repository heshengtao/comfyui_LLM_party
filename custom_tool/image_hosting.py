import base64
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import torch
import locale

def tensor_to_url_sm(image_tensor, api_key):
    """
    将PyTorch张量转换为PNG格式的base64编码字符串并上传至SM.MS图床，返回上传后的图片URL。
    
    参数:
    - image_tensor: PyTorch张量。
    - api_key: SM.MS API密钥。
    
    返回:
    - 图片上传成功后的URL或已存在的图片URL，如果失败则返回None。
    """
    # 确保张量在CPU上，并将其转换为NumPy数组
    if isinstance(image_tensor, torch.Tensor):
        i = 255.0 * image_tensor.cpu().numpy()
    else:
        raise TypeError("Input should be a PyTorch Tensor.")

    # 创建PIL Image对象并保存到内存中的字节流
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 设置上传文件，注意这里使用了'image.png'和'image/png'MIME类型来匹配PNG格式
    files = {'smfile': ('image.png', base64.b64decode(img_str), 'image/png')}
    
    # 设置请求头
    headers = {
        'Authorization': api_key,
    }

    try:
        # 发送POST请求到SM.MS API v2
        response = requests.post('https://sm.ms/api/v2/upload', files=files, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，抛出HTTPError异常
        
        result = response.json()
        if result['success']:
            return result['data']['url']  # 返回上传成功的图片URL
        elif result.get('code') == 'image_repeated':
            # 如果是重复上传，则返回已存在的图片URL
            return result['images']
        else:
            print(f"Error: {result.get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error: {e}")
        return None

def tensor_to_url_imgbb(image_tensor, api_key):
    """
    将PyTorch张量转换为PNG格式的base64编码字符串并上传至imgbb.com图床，返回上传后的图片URL。

    参数:
    - image_tensor: PyTorch张量。
    - api_key: imgbb.com API密钥。

    返回:
    - 图片上传成功后的URL或已存在的图片URL，如果失败则返回None。
    """
    # 确保张量在CPU上，并将其转换为NumPy数组
    if isinstance(image_tensor, torch.Tensor):
        i = 255.0 * image_tensor.cpu().numpy()
    else:
        raise TypeError("Input should be a PyTorch Tensor.")

    # 创建PIL Image对象并保存到内存中的字节流
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": api_key, "image": img_str}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        result = response.json()
        img_url = result["data"]["url"]
        return img_url
    else:
        return "Error: " + response.text

    
def tensor_to_url_imagehub(image_tensor, api_key):
    """
    将PyTorch张量转换为PNG格式并上传至指定图床，返回上传后的图片URL。

    参数:
    - image_tensor: PyTorch张量。
    - api_key: 自定义图床API密钥。

    返回:
    - 图片上传成功后的URL或已存在的图片URL，如果失败则返回错误信息。
    """
    # 确保张量在CPU上，并将其转换为NumPy数组
    if isinstance(image_tensor, torch.Tensor):
        i = 255.0 * image_tensor.cpu().numpy()
    else:
        raise TypeError("Input should be a PyTorch Tensor.")

    # 创建PIL Image对象并保存到内存中的字节流
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)  # 移动到数据的开头

    url = "https://www.imagehub.cc/api/1/upload"
    headers = {
        "X-API-Key": api_key,
    }
    
    files = {
        'source': ('image.png', buffered.getvalue(), 'image/png'),
    }

    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        result = response.json()
        if 'success' in result and result['success']['code'] == 200:
            img_url = result['image']['url']
            return img_url
        else:
            return "Error: Upload failed with message - {}".format(result.get('status_txt', 'Unknown error'))
    else:
        return "Error: HTTP request failed with status code - {}, message - {}".format(response.status_code, response.text)

def tensor_to_url_chevereto(image_tensor, api_key,chevereto_url):
    """
    将PyTorch张量转换为PNG格式并上传至指定图床，返回上传后的图片URL。

    参数:
    - image_tensor: PyTorch张量。
    - api_key: 自定义图床API密钥。

    返回:
    - 图片上传成功后的URL或已存在的图片URL，如果失败则返回错误信息。
    """
    # 确保张量在CPU上，并将其转换为NumPy数组
    if isinstance(image_tensor, torch.Tensor):
        i = 255.0 * image_tensor.cpu().numpy()
    else:
        raise TypeError("Input should be a PyTorch Tensor.")

    # 创建PIL Image对象并保存到内存中的字节流
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)  # 移动到数据的开头

    url = chevereto_url
    headers = {
        "X-API-Key": api_key,
    }
    
    files = {
        'source': ('image.png', buffered.getvalue(), 'image/png'),
    }

    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        result = response.json()
        if 'success' in result and result['success']['code'] == 200:
            img_url = result['image']['url']
            return img_url
        else:
            return "Error: Upload failed with message - {}".format(result.get('status_txt', 'Unknown error'))
    else:
        return "Error: HTTP request failed with status code - {}, message - {}".format(response.status_code, response.text)
    
class img_hosting:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "api_key": ("STRING", {"default":""}), 
                "img_hosting": (["chevereto","sm.ms", "imgbb.com","imagehub.cc"], {"default": "sm.ms"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                },
            "optional": {
                "img_hosting_url": ("STRING", {"default":"http://mysite.com/api/1/upload"}),
            }
            }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("img_URL","is_help",)

    FUNCTION = "convert"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def convert(self,image, api_key, img_hosting, is_enable=True,img_hosting_url=""):
        is_help = "选择chevereto时，需要填入img_hosting_url，这是你自己部署的chevereto的api地址，如果选择其他图床，则不需要填入，需要去对应的图床官网申请api_key\nSelect chevereto, you need to fill in img_hosting_url, which is your own deployment of chevereto API address, if you choose other map, you do not need to fill in, you need to go to the corresponding map official website application api_key"
        if is_enable:
            if img_hosting == "sm.ms":
                return (tensor_to_url_sm(image[0], api_key),is_help,)
            elif img_hosting == "imgbb.com":
                return (tensor_to_url_imgbb(image[0], api_key),is_help,)
            elif img_hosting == "imagehub.cc":
                return (tensor_to_url_imagehub(image[0], api_key),is_help,)
            elif img_hosting == "chevereto":
                return (tensor_to_url_chevereto(image[0], api_key,img_hosting_url),is_help,)
            else:
                return (None,is_help,)
        else:
            return (None,is_help,)
        
NODE_CLASS_MAPPINGS = {"img_hosting": img_hosting}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"img_hosting": "图床"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"img_hosting": "Image Hosting"}