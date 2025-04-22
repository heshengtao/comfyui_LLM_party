import locale
from fish_audio_sdk import Session, ASRRequest, TTSRequest, ReferenceAudio
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
        if api_key is None or api_key == "":
            api_key = config.get("API_KEYS", "fish_api_key")
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
    
class fish_tts:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "input_string": ("STRING", {"default": ""}),
            },
            "optional": {
                "reference_audio_path": ("STRING", {"default": ""}),
                "reference_text": ("STRING", {"default": ""}),
                "reference_id":("STRING", {"default": ""}),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "AUDIO",
    )
    RETURN_NAMES = (
        "audio_path",
        "audio",
    )

    FUNCTION = "tts"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/音频（audio）"

    def tts(self,reference_audio_path="",reference_text="",reference_id="", is_enable=True, input_string="", api_key=None):
        if is_enable == False:
            return (None,)
        if input_string != "":
            # 获得当前时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 判断当前目录是否存在audio文件夹，如果不存在则创建
            if not os.path.exists(os.path.join(current_dir_path, "audio")):
                os.makedirs(os.path.join(current_dir_path, "audio"))
            full_audio_path = os.path.join(current_dir_path, "audio", f"{timestamp}.mp3")
            if api_key is None or api_key == "":
                api_key = config.get("API_KEYS", "fish_api_key")
            session = Session(api_key)

            if reference_audio_path != "":
                with open(reference_audio_path, "rb") as audio_file:
                    with open(full_audio_path, "wb") as f:
                        for chunk in session.tts(TTSRequest(
                            text=input_string,
                            references=[
                                ReferenceAudio(
                                    audio=audio_file.read(),
                                    text=reference_text,
                                )
                            ]
                        )):
                            f.write(chunk)
            elif reference_id != "":
                with open(full_audio_path, "wb") as f:
                    for chunk in session.tts(TTSRequest(
                        reference_id=reference_id,
                        text=input_string
                    )):
                        f.write(chunk)
            out = full_audio_path
            waveform, sample_rate = torchaudio.load(full_audio_path)
            audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        else:
            out = None
        return (
            out,
            audio_out,
        )



NODE_CLASS_MAPPINGS = {
    "fish_whisper": fish_whisper,
    "fish_tts": fish_tts,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'


try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "fish_whisper": "☁️Fish语音识别",
        "fish_tts": "☁️Fish语音合成",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "fish_whisper": "☁️Fish ASR",
        "fish_tts": "☁️Fish TTS",
    }