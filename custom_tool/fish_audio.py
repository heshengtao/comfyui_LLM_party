import locale
from fish_audio_sdk import Session, ASRRequest
import os
import time
import torchaudio

current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
# 设置录音参数
fs = 44100  # 采样率


class fish_whisper:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "audio_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "audio": ("AUDIO", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "whisper"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/音频（audio）"

    def whisper(self,audio_path,is_enable=True,  api_key=None, audio=None):
        if is_enable == False:
            return (None,)
        session = Session(api_key)
        if audio is not None:
            # 获得当前时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 保存录音文件的路径
            audio_path = os.path.join(current_dir_path, "record", f"{timestamp}.wav")
            torchaudio.save(audio_path, audio["waveform"].squeeze(0), audio["sample_rate"])
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
            response = session.asr(ASRRequest(audio=audio_data))
            out = response.text
        elif audio_path != "" and audio_path is not None:
            # 用fish_audio识别音频
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
            response = session.asr(ASRRequest(audio=audio_data))
            out = response.text
        else:
            out = None

        return (out,)
    
NODE_CLASS_MAPPINGS = {
    "fish_whisper": fish_whisper,
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
        "fish_whisper": "Fish语音识别",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "fish_whisper": "Fish Whisper",
    }