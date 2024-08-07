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
    CATEGORY = "大模型派对（llm_party）/绘图（image）"

    def split(self, images,):
      if images is None:
        return (None, None, None, None, None)
      new_images = torch.chunk(images, len(images), dim=0)
      return new_images
    
NODE_CLASS_MAPPINGS = {"Images2Image": Images2Image}
lang = locale.getdefaultlocale()[0]
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"Images2Image": "图像拆分器"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"Images2Image": "Images 2 Image"}