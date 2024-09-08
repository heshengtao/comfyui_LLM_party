import locale
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)


class LLavaLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": ""}),
                "ckpt_path": ("STRING", {"default": ""}),
                "clip_path": ("STRING", {"default": ""}),
                "max_ctx": ("INT", {"default": 2048, "min": 300, "max": 100000, "step": 64}),
                "gpu_layers": ("INT", {"default": 27, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_llava_checkpoint"

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def load_llava_checkpoint(self, model_name, ckpt_path, max_ctx, gpu_layers, n_threads, clip_path):
        from llama_cpp import Llama
        from llama_cpp.llama_chat_format import Llava15ChatHandler
        if ckpt_path != "" and clip_path != "":
            model_name = ""
        if model_name in config:
            ckpt_path = config[model_name].get("ckpt_path")
            clip_path = config[model_name].get("clip_path")
        clip = Llava15ChatHandler(clip_model_path=clip_path, verbose=False)
        llm = Llama(
            model_path=ckpt_path,
            chat_handler=clip,
            offload_kqv=True,
            f16_kv=True,
            use_mlock=False,
            embedding=False,
            n_batch=1024,
            last_n_tokens_size=1024,
            verbose=True,
            seed=42,
            n_ctx=max_ctx,
            n_gpu_layers=gpu_layers,
            n_threads=n_threads,
            logits_all=True,
            echo=False,
        )
        return (llm,)
    
NODE_CLASS_MAPPINGS = {"LLavaLoader":LLavaLoader}
lang = locale.getdefaultlocale()[0]

try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"LLavaLoader": "LLava加载器"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"LLavaLoader": "LLava Loader"}