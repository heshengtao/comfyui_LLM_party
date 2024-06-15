import numpy as np
import torch
from ..lib_omost.canvas import Canvas as omost_canvas
def conditioning_set_values(conditioning, values={}):
    c = []
    for t in conditioning:
        n = [t[0], t[1].copy()]
        for k in values:
            n[1][k] = values[k]
        c.append(n)

    return c
class omost_decode:
    def __init__(self):
        self.device = "cuda"if torch.cuda.is_available()else ("mps" if torch.backends.mps.is_available() else "cpu")
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP",{} ),
                "text": ("STRING", {"forceInput": True}),
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "notify"
    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def notify(self, text,clip):
        canvas = omost_canvas.from_bot_response(text[0])
        canvas_outputs = canvas.process()
        initial_latent=canvas_outputs['initial_latent']
        input_data = np.array(initial_latent)
        # 获取输入数据的高度和宽度
        height, width, _ = input_data.shape
        latent_shape = (1, 4, height, width)
        latent = torch.zeros(latent_shape, device=self.device)
        for i in range(3):
            latent[0, i, :, :] = torch.from_numpy(input_data[:, :, i % 3])
        bag_of_conditions=canvas_outputs['bag_of_conditions']
        # 创建一个空列表来收集mask_tensor
        c_list=[]
        # 循环遍历bag_of_conditions中的每个条件
        for cond in bag_of_conditions:
            mask_np = cond['mask']
            # 将NumPy数组转换为PyTorch张量，并添加一个新的维度
            mask_tensor = torch.from_numpy(mask_np).float().unsqueeze(0)
            # 将mask_tensor添加到列表中
            prefixes=cond['prefixes']
            suffixes=cond['suffixes']
            for target in suffixes:
                prompt = "".join(prefixes + [target])
            tokens = clip[0].tokenize(prompt)
            condition, pooled = clip[0].encode_from_tokens(tokens, return_pooled=True)
            cd=[[condition, {"pooled_output": pooled}]]
            c = conditioning_set_values(cd, {"mask": mask_tensor,
                                            "set_area_to_bounds":False,
                                            "mask_strength": 1.0})
            c_list.extend(c)  
        return (c_list,)
    