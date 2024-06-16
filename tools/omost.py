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
                "mode": (["fusion","block"],{"default":"fusion"}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("CONDITIONING","MASK",)
    RETURN_NAMES = ("conditioning","mask",)
    FUNCTION = "notify"
    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def notify(self, text,clip,mode="fusion",strength=1.0):
        canvas = omost_canvas.from_bot_response(text[0])
        canvas_outputs = canvas.process()
        #initial_latent=torch.from_numpy(canvas_outputs['initial_latent']).unsqueeze(0)
        #t = vae[0].encode(initial_latent[:,:,:,:3])

        bag_of_conditions=canvas_outputs['bag_of_conditions']
        # 创建一个空列表来收集mask_tensor
        c_list=[]
        mask_tensors=[]
        condition_list=[]
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
            condition_list.append(condition)
            cd=[[condition, {"pooled_output": pooled}]]
            c = conditioning_set_values(cd, {"mask": mask_tensor,
                                            "set_area_to_bounds":False,
                                            "mask_strength": strength[0]})
            c_list.extend(c)  
            mask_tensors.append(mask_tensor)
        # mask_tensors全部相加，形状不变，然后除以mask_tensors的个数
        mask_tensor_out = torch.stack(mask_tensors).sum(dim=0) / len(mask_tensors)
        
        if mode=="fusion":
            conditions = torch.cat(condition_list, dim=1)
            cd = [[conditions, {"pooled_output": pooled}]]
            c_list = conditioning_set_values(cd, {"mask": mask_tensor_out,
                                            "set_area_to_bounds":False,
                                            "mask_strength": strength[0]})
        return (c_list ,mask_tensor_out,)
    
class omost_setting:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "color": ([
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black',
    'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse',
    'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue',
    'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki',
    'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon',
    'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise',
    'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
    'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod',
    'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
    'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue',
    'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen',
    'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
    'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta',
    'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple',
    'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
    'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite',
    'navy', 'navyblue', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid',
    'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff',
    'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown',
    'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna',
    'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen',
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white',
    'whitesmoke', 'yellow', 'yellowgreen'
],{"default":'aliceblue'}),
                "locations": ([
    'in the center', 'on the left', 'on the right', 'on the top', 'on the bottom',
    'on the top-left', 'on the top-right', 'on the bottom-left', 'on the bottom-right'
],{"default":'in the center'}),
                "offsets": ([
    'no offset', 'slightly to the left', 'slightly to the right', 'slightly to the upper',
    'slightly to the lower', 'slightly to the upper-left', 'slightly to the upper-right',
    'slightly to the lower-left', 'slightly to the lower-right'
],{"default":'no offset'}),
                "areas": ([
    'a small square area', 'a small vertical area', 'a small horizontal area',
    'a medium-sized square area', 'a medium-sized vertical area', 'a medium-sized horizontal area',
    'a large square area', 'a large vertical area', 'a large horizontal area'
],{"default":'a small square area'}),
            },
        }

    RETURN_TYPES = (
        "STRING",
    )
    RETURN_NAMES = (
        "string",
    )

    FUNCTION = "substr"

    #OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def substr(self, color, locations, offsets, areas):
        out =f"""location='{locations}',
offset='{offsets}',
area='{areas}',
HTML_web_color_name='{color}',
"""
        return (
            out,
        )
    