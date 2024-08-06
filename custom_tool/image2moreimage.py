import locale


class Split_image_batch:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE",),
            "batch_size": (
                "INT", {"default": 0, "step": 1,
            })
            }}

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "decode"

    CATEGORY = "大模型派对（llm_party）/绘图（image）"

    def decode(self, images, batch_size=0):
        if images == None or images == []:
            return (None,)
        elif len(images) > 1:
            image = images[batch_size]
        else:
            image = image
            return (image,)
NODE_CLASS_MAPPINGS = {
    "Split_image_batch": Split_image_batch,
}
lang = locale.getdefaultlocale()[0]
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Split_image_batch": "拆分图片批次"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Split_image_batch": "Split image batch"
    }