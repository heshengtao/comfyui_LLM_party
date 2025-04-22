import locale
import torch
class Images2Image:
    @classmethod
    def INPUT_TYPES(s):
        return {
          "required": {
              "images": ("IMAGE",),
          }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("image1", "image2", "image3", "image4", "image5")
    FUNCTION = "split"
    CATEGORY = "大模型派对（llm_party）/图片（image）"

    def split(self, images,):
      if images is None:
        return (None, None, None, None, None)
      new_images = torch.chunk(images, len(images), dim=0)
      return new_images
    
NODE_CLASS_MAPPINGS = {"Images2Image": Images2Image}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"Images2Image": "图像拆分器"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"Images2Image": "Images 2 Image"}