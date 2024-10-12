import gc
import sys

import requests
import torch


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


class clear_model:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any": (any_type, {}),
                "model": ("CUSTOM", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "tokenizer": (
                    "CUSTOM",
                    {
                        "default": None,
                    },
                ),
                "is_ollama": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("any",)

    FUNCTION = "clear"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def clear(self, any, model,is_enable, tokenizer=None,is_ollama=False):
        if not is_enable:
            return (None,)
        out = any
        if is_ollama:
            url = "http://127.0.0.1:11434/api/generate"
            payload = {
                "model": model.model_name,
                "keep_alive": 0
            }
            response = requests.post(url, json=payload)
            print(response.json())
            return (out,)
        print(f"After function call, reference count: {sys.getrefcount(model)}")

        # 查找所有引用
        def find_references(obj):
            refs = []
            for ref in gc.get_referrers(obj):
                if isinstance(ref, dict):
                    for key, value in ref.items():
                        if value is obj:
                            refs.append((ref, key))
                elif isinstance(ref, list):
                    for i, value in enumerate(ref):
                        if value is obj:
                            refs.append((ref, i))
                elif isinstance(ref, tuple):
                    pass
                elif isinstance(ref, set):
                    for value in ref:
                        if value is obj:
                            refs.append((ref, None))
                elif isinstance(ref, frozenset):
                    for value in ref:
                        if value is obj:
                            refs.append((ref, None))
                elif hasattr(ref, "__dict__"):
                    # 如果ref.model存在
                    if hasattr(ref, "model"):
                        ref.model = None
                    # 如果ref.tokenizer存在
                    if hasattr(ref, "tokenizer"):
                        ref.tokenizer = None
            return refs

        # 获取所有引用
        references = find_references(model)
        print(f"Found {len(references)} references.")
        model = None
        # 清除所有引用
        for ref, key in references:
            ref[key] = None

        if tokenizer != None:
            references = find_references(tokenizer)
            print(f"Found {len(references)} references.")
            tokenizer = None
        # 显式调用垃圾回收
        gc.collect()
        # 回收显存
        torch.cuda.empty_cache()
        return (out,)
