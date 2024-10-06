import locale
import os
import sys

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser

import torch
from transformers import AutoConfig, AutoModelForPreTraining, AutoProcessor

if torch.cuda.is_available():
    from transformers import BitsAndBytesConfig
config = configparser.ConfigParser()
config.read(config_path)


class LLavaLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_path": ("STRING", {"default": ""}),
                "clip_path": ("STRING", {"default": ""}),
                "max_ctx": ("INT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
                "gpu_layers": ("INT", {"default": 31, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_llava_checkpoint"

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def load_llava_checkpoint(self, ckpt_path, clip_path, max_ctx, gpu_layers, n_threads):
        from llama_cpp import Llama
        from llama_cpp.llama_chat_format import Llava15ChatHandler

        clip = Llava15ChatHandler(clip_model_path=clip_path, verbose=False)
        llm = Llama(
            model_path=ckpt_path,
            chat_handler=clip,
            n_ctx=max_ctx,
            n_gpu_layers=gpu_layers,
            n_threads=n_threads,
        )
        return (llm,)


class GGUFLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default": ""}),
                "max_ctx": ("INT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
                "gpu_layers": ("INT", {"default": 31, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_GGUF_checkpoint"

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def load_GGUF_checkpoint(self, model_path, max_ctx, gpu_layers, n_threads):
        from llama_cpp import Llama

        llm = Llama(
            model_path,
            n_ctx=max_ctx,
            n_gpu_layers=gpu_layers,
            n_threads=n_threads,
        )
        return (llm,)


class vlmLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name_or_path": ("STRING", {"default": ""}),
                "device": (
                    ["auto", "cuda", "cpu", "mps"],
                    {
                        "default": "auto",
                    },
                ),
                "dtype": (
                    ["float32", "float16", "bfloat16", "int8", "int4"],
                    {
                        "default": "float32",
                    },
                ),
            }
        }

    RETURN_TYPES = (
        "CUSTOM",
        "CUSTOM",
    )
    RETURN_NAMES = (
        "model",
        "tokenizer(processor)",
    )
    FUNCTION = "load_VLM"

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def load_VLM(self, model_name_or_path, device, dtype):
        model_kwargs = {
            "device_map": device,
        }

        if dtype == "float16":
            model_kwargs["torch_dtype"] = torch.float16
        elif dtype == "bfloat16":
            model_kwargs["torch_dtype"] = torch.bfloat16
        elif dtype in ["int8", "int4"]:
            model_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_8bit=(dtype == "int8"), load_in_4bit=(dtype == "int4")
            )

        config = AutoConfig.from_pretrained(model_name_or_path, **model_kwargs)
        processor = AutoProcessor.from_pretrained(model_name_or_path)
        model = AutoModelForPreTraining.from_pretrained(model_name_or_path, **model_kwargs)
        model = model.eval()
        return (
            model,
            processor,
        )


NODE_CLASS_MAPPINGS = {
    "LLavaLoader": LLavaLoader,
    "GGUFLoader": GGUFLoader,
    "vlmLoader": vlmLoader,
}
lang = locale.getdefaultlocale()[0]

try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language == "en_US":
    lang = language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "LLavaLoader": "VLM-GGUF加载器",
        "GGUFLoader": "LLM-GGUF加载器",
        "vlmLoader": "VLM本地加载器",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "LLavaLoader": "VLM-GGUF Loader",
        "GGUFLoader": "LLM-GGUF Loader",
        "vlmLoader": "VLM local Loader",
    }
