import locale
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
from transformers import AutoProcessor, AutoModelForPreTraining,AutoConfig
import torch
if torch.cuda.is_available():
    from transformers import BitsAndBytesConfig
config = configparser.ConfigParser()
config.read(config_path)
VLM_dir= os.path.join(current_dir, "model","VLM")
VLM_list = [f for f in os.listdir(VLM_dir) if os.path.isdir(os.path.join(VLM_dir, f))]

VLM_GGUF_dir= os.path.join(current_dir, "model","VLM-GGUF")
VLM_GGUF_list= []
for root, dirs, files in os.walk(VLM_GGUF_dir):
    for file in files:
        if file.endswith(".gguf") or file.endswith(".GGUF"):
            VLM_GGUF_list.append(os.path.join(root, file))

LLM_GGUF_dir= os.path.join(current_dir, "model","LLM-GGUF")
LLM_GGUF_list= []
for root, dirs, files in os.walk(LLM_GGUF_dir):
    for file in files:
        if file.endswith(".gguf") or file.endswith(".GGUF"):
            LLM_GGUF_list.append(os.path.join(root, file))

class LLavaLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_path": ("STRING", {"default": ""}),
                "clip_path": ("STRING", {"default": ""}),
                "max_ctx":  ("INT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
                "gpu_layers": ("INT", {"default": 31, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
                "chat_format": (["llava-1-5","llava-1-6","llama-3-vision-alpha","minicpm-v-2.6","obsidian","moondream","nanollava"], {"default": "llava-1-5"}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_llava_checkpoint"

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def load_llava_checkpoint(self, ckpt_path, clip_path, max_ctx, gpu_layers, n_threads, chat_format):
        import llama_cpp
        from llama_cpp import Llama
        if chat_format == "llava-1-5":
            clip = llama_cpp.llama_chat_format.Llava15ChatHandler(clip_model_path=clip_path, verbose=False)
        elif chat_format == "llava-1-6":
            clip = llama_cpp.llama_chat_format.Llava16ChatHandler(clip_model_path=clip_path, verbose=False)
        elif chat_format == "llama-3-vision-alpha":
            clip = llama_cpp.llama_chat_format.Llama3VisionAlphaChatHandler(clip_model_path=clip_path, verbose=False)
        elif chat_format == "minicpm-v-2.6":
            clip = llama_cpp.llama_chat_format.MiniCPMv26ChatHandler(clip_model_path=clip_path, verbose=False)
        elif chat_format == "obsidian":
            clip = llama_cpp.llama_chat_format.ObsidianChatHandler(clip_model_path=clip_path, verbose=False)
        elif chat_format == "moondream":
            clip = llama_cpp.llama_chat_format.MoondreamChatHandler(clip_model_path=clip_path, verbose=False)
        elif chat_format == "nanollava":
            clip = llama_cpp.llama_chat_format.NanoLlavaChatHandler(clip_model_path=clip_path, verbose=False)
        
        llm = Llama(
            model_path=ckpt_path,
            chat_handler=clip,
            n_ctx=max_ctx,
            n_gpu_layers=gpu_layers,
            n_threads=n_threads,
        )
        return (llm,)

class easy_LLavaLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_path": (VLM_GGUF_list, {"default": ""}),
                "clip_path": (VLM_GGUF_list, {"default": ""}),
                "max_ctx":  ("INT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
                "gpu_layers": ("INT", {"default": 31, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_llava_checkpoint"

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def load_llava_checkpoint(self, ckpt_path, clip_path, max_ctx, gpu_layers, n_threads):
        from llama_cpp import Llama
        from llama_cpp.llama_chat_format import Llava15ChatHandler
        ckpt_path=os.path.join(VLM_GGUF_dir, ckpt_path)
        clip_path=os.path.join(VLM_GGUF_dir, clip_path)
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

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def load_GGUF_checkpoint(self, model_path, max_ctx, gpu_layers, n_threads):
        from llama_cpp import Llama
        llm = Llama(
            model_path,
            n_ctx=max_ctx,
            n_gpu_layers=gpu_layers,
            n_threads=n_threads,
        )
        return (llm,)

class easy_GGUFLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": (LLM_GGUF_list, {"default": ""}),
                "max_ctx": ("INT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
                "gpu_layers": ("INT", {"default": 31, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_GGUF_checkpoint"

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def load_GGUF_checkpoint(self, model_path, max_ctx, gpu_layers, n_threads):
        from llama_cpp import Llama
        model_path=os.path.join(LLM_GGUF_dir, model_path)
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
                    ["float32", "float16","bfloat16", "int8", "int4"],
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

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def load_VLM(self, model_name_or_path, device, dtype):
        model_kwargs = {
            'device_map': device,
        }

        if dtype == "float16":
            model_kwargs['torch_dtype'] = torch.float16
        elif dtype == "bfloat16":
            model_kwargs['torch_dtype'] = torch.bfloat16
        elif dtype in ["int8", "int4"]:
            model_kwargs['quantization_config'] = BitsAndBytesConfig(load_in_8bit=(dtype == "int8"), load_in_4bit=(dtype == "int4"))

        config = AutoConfig.from_pretrained(model_name_or_path, **model_kwargs)
        processor = AutoProcessor.from_pretrained(model_name_or_path)
        model = AutoModelForPreTraining.from_pretrained(model_name_or_path, **model_kwargs)
        model = model.eval()
        return (
            model,
            processor,
        )

class easy_vlmLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name_or_path": (VLM_list, {"default": ""}),
                "device": (
                    ["auto", "cuda", "cpu", "mps"],
                    {
                        "default": "auto",
                    },
                ),
                "dtype": (
                    ["float32", "float16","bfloat16", "int8", "int4"],
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

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def load_VLM(self, model_name_or_path, device, dtype):
        model_name_or_path=os.path.join(VLM_dir, model_name_or_path)
        model_kwargs = {
            'device_map': device,
        }

        if dtype == "float16":
            model_kwargs['torch_dtype'] = torch.float16
        elif dtype == "bfloat16":
            model_kwargs['torch_dtype'] = torch.bfloat16
        elif dtype in ["int8", "int4"]:
            model_kwargs['quantization_config'] = BitsAndBytesConfig(load_in_8bit=(dtype == "int8"), load_in_4bit=(dtype == "int4"))

        config = AutoConfig.from_pretrained(model_name_or_path, **model_kwargs)
        processor = AutoProcessor.from_pretrained(model_name_or_path)
        model = AutoModelForPreTraining.from_pretrained(model_name_or_path, **model_kwargs)
        model = model.eval()
        return (
            model,
            processor,
        )

NODE_CLASS_MAPPINGS = {
    "LLavaLoader":LLavaLoader,
    "GGUFLoader":GGUFLoader,
    "vlmLoader":vlmLoader,
    "easy_LLavaLoader": easy_LLavaLoader,
    "easy_GGUFLoader":easy_GGUFLoader,
    "easy_vlmLoader":easy_vlmLoader,
    }
lang = locale.getdefaultlocale()[0]

try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "LLavaLoader": "🖥️VLM-GGUF加载器",
        "GGUFLoader": "🖥️LLM-GGUF加载器",
        "vlmLoader": "🖥️VLM本地加载器",
        "easy_LLavaLoader": "🖥️简易VLM-GGUF加载器",
        "easy_GGUFLoader": "🖥️简易LLM-GGUF加载器",
        "easy_vlmLoader": "🖥️简易VLM本地加载器",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "LLavaLoader": "🖥️VLM-GGUF Loader",
        "GGUFLoader": "🖥️LLM-GGUF Loader",
        "vlmLoader": "🖥️VLM local Loader",
        "easy_LLavaLoader": "🖥️Easy VLM-GGUF Loader",
        "easy_GGUFLoader": "🖥️Easy LLM-GGUF Loader",
        "easy_vlmLoader": "🖥️Easy VLM local Loader",
        }