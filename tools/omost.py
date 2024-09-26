import copy

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
        self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        self.text_encoder = None
        self.text_encoder_2 = None
        self.tokenizer = None
        self.tokenizer_2 = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP", {}),
                "text": ("STRING", {"forceInput": True}),
                "mode": (["greedy", "fusion", "block"], {"default": "greedy"}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = (
        "CONDITIONING",
        "MASK",
    )
    RETURN_NAMES = (
        "conditioning",
        "mask",
    )
    FUNCTION = "notify"
    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/图片（image）"

    def notify(self, text, clip, mode="greedy", strength=1.0):
        self.text_encoder = clip[0].encode_from_tokens
        self.tokenizer = clip[0].tokenize
        self.text_encoder_2 = clip[0].encode_from_tokens
        self.tokenizer_2 = clip[0].tokenize
        canvas = omost_canvas.from_bot_response(text[0])
        canvas_outputs = canvas.process()
        # initial_latent=torch.from_numpy(canvas_outputs['initial_latent']).unsqueeze(0)
        # t = vae[0].encode(initial_latent[:,:,:,:3])

        bag_of_conditions = canvas_outputs["bag_of_conditions"]
        # 创建一个空列表来收集mask_tensor
        c_list = []
        mask_tensors = []
        condition_list = []
        # 循环遍历bag_of_conditions中的每个条件
        for cond in bag_of_conditions:
            mask_np = cond["mask"]
            # 将NumPy数组转换为PyTorch张量，并添加一个新的维度
            mask_tensor = torch.from_numpy(mask_np).float().unsqueeze(0)
            # 将mask_tensor添加到列表中
            prefixes = cond["prefixes"]
            suffixes = cond["suffixes"]
            for target in suffixes:
                prompt = "".join(prefixes + [target])
            tokens = clip[0].tokenize(prompt)
            condition, pooled = clip[0].encode_from_tokens(tokens, return_pooled=True)
            condition_list.append(condition)
            cd = [[condition, {"pooled_output": pooled}]]
            c = conditioning_set_values(
                cd, {"mask": mask_tensor, "set_area_to_bounds": False, "mask_strength": strength[0]}
            )
            c_list.extend(c)
            mask_tensors.append(mask_tensor)
        # mask_tensors全部相加，形状不变，然后除以mask_tensors的个数
        mask_tensor_out = torch.stack(mask_tensors).sum(dim=0) / len(mask_tensors)

        if mode == "fusion":
            conditions = torch.cat(condition_list, dim=1)
            cd = [[conditions, {"pooled_output": pooled}]]
            c_list = conditioning_set_values(
                cd, {"mask": mask_tensor_out, "set_area_to_bounds": False, "mask_strength": strength[0]}
            )
        elif mode == "greedy":

            def encode_bag_of_subprompts_greedy(self, prefixes: list[str], suffixes: list[str]):
                device = self.device

                @torch.inference_mode()
                def greedy_partition(items, max_sum):
                    bags = []
                    current_bag = []
                    current_sum = 0

                    for item in items:
                        num = item["length"]
                        if current_sum + num > max_sum:
                            if current_bag:
                                bags.append(current_bag)
                            current_bag = [item]
                            current_sum = num
                        else:
                            current_bag.append(item)
                            current_sum += num

                    if current_bag:
                        bags.append(current_bag)

                    return bags

                @torch.inference_mode()
                def get_77_tokens_in_torch(subprompt_inds, tokenizer):
                    # Note that all subprompt are theoretically less than 75 tokens (without bos/eos)
                    result = (
                        [tokenizer.bos_token_id]
                        + subprompt_inds[:75]
                        + [tokenizer.eos_token_id]
                        + [tokenizer.pad_token_id] * 75
                    )
                    result = result[:77]
                    result = torch.tensor([result]).to(device=device, dtype=torch.int64)
                    return result

                @torch.inference_mode()
                def merge_with_prefix(bag):
                    merged_ids_t1 = copy.deepcopy(prefix_ids_t1)
                    merged_ids_t2 = copy.deepcopy(prefix_ids_t2)

                    for item in bag:
                        merged_ids_t1.extend(item["ids_t1"])
                        merged_ids_t2.extend(item["ids_t2"])

                    return dict(
                        ids_t1=get_77_tokens_in_torch(merged_ids_t1, self.tokenizer),
                        ids_t2=get_77_tokens_in_torch(merged_ids_t2, self.tokenizer_2),
                    )

                @torch.inference_mode()
                def double_encode(pair_of_inds):
                    inds = [pair_of_inds["ids_t1"], pair_of_inds["ids_t2"]]
                    text_encoders = [self.text_encoder, self.text_encoder_2]

                    pooled_prompt_embeds = None
                    prompt_embeds_list = []

                    for text_input_ids, text_encoder in zip(inds, text_encoders):
                        prompt_embeds = text_encoder(text_input_ids, output_hidden_states=True)

                        # Only last pooler_output is needed
                        pooled_prompt_embeds = prompt_embeds.pooler_output

                        # "2" because SDXL always indexes from the penultimate layer.
                        prompt_embeds = prompt_embeds.hidden_states[-2]
                        prompt_embeds_list.append(prompt_embeds)

                    prompt_embeds = torch.concat(prompt_embeds_list, dim=-1)
                    return prompt_embeds, pooled_prompt_embeds

                # Begin with tokenizing prefixes

                prefix_length = 0
                prefix_ids_t1 = []
                prefix_ids_t2 = []

                for prefix in prefixes:
                    ids_t1 = self.tokenizer(prefix, truncation=False, add_special_tokens=False).input_ids
                    ids_t2 = self.tokenizer_2(prefix, truncation=False, add_special_tokens=False).input_ids
                    assert len(ids_t1) == len(ids_t2)
                    prefix_length += len(ids_t1)
                    prefix_ids_t1 += ids_t1
                    prefix_ids_t2 += ids_t2

                # Then tokenizing suffixes

                allowed_suffix_length = 75 - prefix_length
                suffix_targets = []

                for subprompt in suffixes:
                    # Note that all subprompt are theoretically less than 75 tokens (without bos/eos)
                    # So we can safely just crop it to 75
                    ids_t1 = self.tokenizer(subprompt, truncation=False, add_special_tokens=False).input_ids[:75]
                    ids_t2 = self.tokenizer_2(subprompt, truncation=False, add_special_tokens=False).input_ids[:75]
                    assert len(ids_t1) == len(ids_t2)
                    suffix_targets.append(dict(length=len(ids_t1), ids_t1=ids_t1, ids_t2=ids_t2))

                # Then merge prefix and suffix tokens

                suffix_targets = greedy_partition(suffix_targets, max_sum=allowed_suffix_length)
                targets = [merge_with_prefix(b) for b in suffix_targets]

                # Encode!

                conds, poolers = [], []

                for target in targets:
                    cond, pooler = double_encode(target)
                    conds.append(cond)
                    poolers.append(pooler)

                conds_merged = torch.concat(conds, dim=1)
                poolers_merged = poolers[0]

                return dict(cond=conds_merged, pooler=poolers_merged)

            encoder_output = encode_bag_of_subprompts_greedy(prefixes=prefixes, suffixes=suffixes)
            c_list = [
                [
                    encoder_output.cond,
                    {"pooled_output": encoder_output.pooler},
                ]
            ]
        return (
            c_list,
            mask_tensor_out,
        )


class omost_setting:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "color": (
                    [
                        "aliceblue",
                        "antiquewhite",
                        "aqua",
                        "aquamarine",
                        "azure",
                        "beige",
                        "bisque",
                        "black",
                        "blanchedalmond",
                        "blue",
                        "blueviolet",
                        "brown",
                        "burlywood",
                        "cadetblue",
                        "chartreuse",
                        "chocolate",
                        "coral",
                        "cornflowerblue",
                        "cornsilk",
                        "crimson",
                        "cyan",
                        "darkblue",
                        "darkcyan",
                        "darkgoldenrod",
                        "darkgray",
                        "darkgrey",
                        "darkgreen",
                        "darkkhaki",
                        "darkmagenta",
                        "darkolivegreen",
                        "darkorange",
                        "darkorchid",
                        "darkred",
                        "darksalmon",
                        "darkseagreen",
                        "darkslateblue",
                        "darkslategray",
                        "darkslategrey",
                        "darkturquoise",
                        "darkviolet",
                        "deeppink",
                        "deepskyblue",
                        "dimgray",
                        "dimgrey",
                        "dodgerblue",
                        "firebrick",
                        "floralwhite",
                        "forestgreen",
                        "fuchsia",
                        "gainsboro",
                        "ghostwhite",
                        "gold",
                        "goldenrod",
                        "gray",
                        "grey",
                        "green",
                        "greenyellow",
                        "honeydew",
                        "hotpink",
                        "indianred",
                        "indigo",
                        "ivory",
                        "khaki",
                        "lavender",
                        "lavenderblush",
                        "lawngreen",
                        "lemonchiffon",
                        "lightblue",
                        "lightcoral",
                        "lightcyan",
                        "lightgoldenrodyellow",
                        "lightgray",
                        "lightgrey",
                        "lightgreen",
                        "lightpink",
                        "lightsalmon",
                        "lightseagreen",
                        "lightskyblue",
                        "lightslategray",
                        "lightslategrey",
                        "lightsteelblue",
                        "lightyellow",
                        "lime",
                        "limegreen",
                        "linen",
                        "magenta",
                        "maroon",
                        "mediumaquamarine",
                        "mediumblue",
                        "mediumorchid",
                        "mediumpurple",
                        "mediumseagreen",
                        "mediumslateblue",
                        "mediumspringgreen",
                        "mediumturquoise",
                        "mediumvioletred",
                        "midnightblue",
                        "mintcream",
                        "mistyrose",
                        "moccasin",
                        "navajowhite",
                        "navy",
                        "navyblue",
                        "oldlace",
                        "olive",
                        "olivedrab",
                        "orange",
                        "orangered",
                        "orchid",
                        "palegoldenrod",
                        "palegreen",
                        "paleturquoise",
                        "palevioletred",
                        "papayawhip",
                        "peachpuff",
                        "peru",
                        "pink",
                        "plum",
                        "powderblue",
                        "purple",
                        "rebeccapurple",
                        "red",
                        "rosybrown",
                        "royalblue",
                        "saddlebrown",
                        "salmon",
                        "sandybrown",
                        "seagreen",
                        "seashell",
                        "sienna",
                        "silver",
                        "skyblue",
                        "slateblue",
                        "slategray",
                        "slategrey",
                        "snow",
                        "springgreen",
                        "steelblue",
                        "tan",
                        "teal",
                        "thistle",
                        "tomato",
                        "turquoise",
                        "violet",
                        "wheat",
                        "white",
                        "whitesmoke",
                        "yellow",
                        "yellowgreen",
                    ],
                    {"default": "aliceblue"},
                ),
                "locations": (
                    [
                        "in the center",
                        "on the left",
                        "on the right",
                        "on the top",
                        "on the bottom",
                        "on the top-left",
                        "on the top-right",
                        "on the bottom-left",
                        "on the bottom-right",
                    ],
                    {"default": "in the center"},
                ),
                "offsets": (
                    [
                        "no offset",
                        "slightly to the left",
                        "slightly to the right",
                        "slightly to the upper",
                        "slightly to the lower",
                        "slightly to the upper-left",
                        "slightly to the upper-right",
                        "slightly to the lower-left",
                        "slightly to the lower-right",
                    ],
                    {"default": "no offset"},
                ),
                "areas": (
                    [
                        "a small square area",
                        "a small vertical area",
                        "a small horizontal area",
                        "a medium-sized square area",
                        "a medium-sized vertical area",
                        "a medium-sized horizontal area",
                        "a large square area",
                        "a large vertical area",
                        "a large horizontal area",
                    ],
                    {"default": "a small square area"},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)

    FUNCTION = "substr"

    # OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/图片（image）"

    def substr(self, color, locations, offsets, areas):
        out = f"""location='{locations}',
offset='{offsets}',
area='{areas}',
HTML_web_color_name='{color}',
"""
        return (out,)
