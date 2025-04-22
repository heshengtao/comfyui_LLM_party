import locale


class extra_parameters:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_out": ("BOOLEAN", {"default": False}),
                "n": ("INT", {"default": 1}),
                "stop": ("STRING", {"default": ""}),
                "presence_penalty": ("FLOAT", {"default": 0.0,"min": 0.0, "max": 1.0,"step": 0.1}),
                "frequency_penalty": ("FLOAT", {"default": 0.0,"min": 0.0, "max": 1.0,"step": 0.1}),
                "repetition_penalty": ("FLOAT", {"default": 1.0,"min": 0.0, "max": 1.0,"step": 0.1}),
                "min_length": ("INT", {"default": 0}),
                "logprobs": ("BOOLEAN", {"default": False}),
                "echo": ("BOOLEAN", {"default": False}),
                "best_of": ("INT", {"default": 1}),
                "user": ("STRING", {"default": ""}),
                "top_p": ("FLOAT", {"default": 1.0,"min": 0.0, "max": 1.0,"step": 0.1}),
                "top_k": ("INT", {"default": 50}),
                "seed": ("INT", {"default": 42}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("extra_parameters",)

    FUNCTION = "extra"

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def extra(
        self,
        top_p=1.0,
        n=1,
        stop="",
        presence_penalty=0.0,
        frequency_penalty=0.0,
        logprobs=False,
        echo=False,
        best_of=1,
        user="",
        json_out=False,
        top_k=50,
        min_length=0,
        repetition_penalty=1.0,
        seed=42,
    ):
        json_data = {}
        if top_p != 1.0:
            json_data["top_p"] = top_p
        if n != 1:
            json_data["n"] = n
        if stop:
            json_data["stop"] = stop
        if presence_penalty != 0.0:
            json_data["presence_penalty"] = presence_penalty
        if frequency_penalty != 0.0:
            json_data["frequency_penalty"] = frequency_penalty
        if logprobs:
            json_data["logprobs"] = logprobs
        if echo:
            json_data["echo"] = echo
        if best_of != 1:
            json_data["best_of"] = best_of
        if user:
            json_data["user"] = user
        if json_out:
            json_data["response_format"] = {"type": "json_object"}
        if top_k != 50:
            json_data["top_k"] = top_k
        if min_length != 0:
            json_data["min_length"] = min_length
        if repetition_penalty != 1.0:
            json_data["repetition_penalty"] = repetition_penalty
        if seed != 42:
            json_data["seed"] = seed

        return (json_data,)


NODE_CLASS_MAPPINGS = {"extra_parameters": extra_parameters}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"extra_parameters": "额外模型参数"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"extra_parameters": "Extra Model Parameters"}
