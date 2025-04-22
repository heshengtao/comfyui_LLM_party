# Use a pipeline as a high-level helper
import locale
import time
import torch
import torchaudio
from transformers import pipeline
import os
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class whisper_local:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "model_name_or_path": ("STRING", {"default": "openai/whisper-small"}),
            "audio": ("AUDIO", {}),
            "is_enable": ("BOOLEAN", {"default": True}),
            "audio_path": ("STRING", {"default": ""}),
            }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "大模型派对（llm_party）/音频（audio）"

    def save(self, model_name_or_path, audio,audio_path, is_enable=True):
        if is_enable is False:
            return (None,)
        device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        pipe = pipeline("automatic-speech-recognition", model=model_name_or_path,device=device)
        if audio is not None:
            # 获得当前时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 保存录音文件的路径
            audio_path = os.path.join(current_dir_path, "record", f"{timestamp}.wav")
            # audio_out再保存回文件
            torchaudio.save(audio_path, audio["waveform"].squeeze(0), audio["sample_rate"])
            # Use the pipeline as a function
            result = pipe(audio_path)
        elif   audio_path != "" and audio_path is not None:
            result = pipe(audio_path)
        else:
            return (None,)

        return (result['text'],)


NODE_CLASS_MAPPINGS = {"whisper_local": whisper_local}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"whisper_local": "🖥️语音转文字本地模型"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"whisper_local": "🖥️Speech to Text Local Model"}