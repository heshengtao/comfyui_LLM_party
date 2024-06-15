import numpy as np
import torch
from ..lib_omost.canvas import Canvas as omost_canvas
import torch.nn.functional as F

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
    RETURN_TYPES = ("CONDITIONING","MASK",)
    RETURN_NAMES = ("conditioning","mask",)
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
        mask_tensors = []
        conditions=[]
        # 循环遍历bag_of_conditions中的每个条件
        for cond in bag_of_conditions:
            mask_np = cond['mask']
            # 将NumPy数组转换为PyTorch张量，并添加一个新的维度
            mask_tensor = torch.from_numpy(mask_np).float().unsqueeze(0)
            # 将mask_tensor添加到列表中
            mask_tensors.append(mask_tensor)
            prefixes=cond['prefixes']
            suffixes=cond['suffixes']
            for target in suffixes:
                prompt = "".join(prefixes + [target])
            tokens = clip[0].tokenize(prompt)
            condition, pooled = clip[0].encode_from_tokens(tokens, return_pooled=True)
            conditions.append(condition)
        # 使用torch.cat沿着第1维合并所有的conditions
        condition_out = torch.cat(conditions, dim=1)
        # mask_tensors里所有张量直接相加，形状不变，再除以列表长度
        combined_mask_tensor = torch.cat(mask_tensors, dim=0).sum(dim=0) / len(mask_tensors)
        return ([[condition_out, {"pooled_output": pooled}]],combined_mask_tensor,)
    

