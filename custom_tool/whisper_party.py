import base64
import datetime
import hashlib
import io
import locale
import os
import time

import folder_paths
import keyboard
import openai
import requests
import sounddevice as sd
import torchaudio
from openai import OpenAI,AzureOpenAI
import soundfile as sf

current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
# 设置录音参数
fs = 44100  # 采样率

if not os.path.exists(os.path.join(current_dir_path, "record")):
    os.makedirs(os.path.join(current_dir_path, "record"))


# 录音函数
def record_audio():
    print("开始录音...")
    recording = sd.rec(int(fs * 10), samplerate=fs, channels=2)
    sd.wait()  # 等待录音结束
    return recording


# 保存录音文件
def save_recording(recording, file_path):
    sf.write(file_path, recording, fs)  # 直接保存为wav文件
    print(f"录音已保存到：{file_path}")


class listen_audio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "press_key": (
                    ["shift", "space", "ctrl", "alt", "tab"],
                    {
                        "default": "shift",
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

    FUNCTION = "listen"

    # OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/音频（audio）"

    def listen(self, press_key="shift"):
        print(f"请按下{press_key}键开始录音，松开后录音结束。")
        while True:  # 持续监听键盘
            try:
                if keyboard.is_pressed(press_key):  # 如果按下空格键
                    audio_data = record_audio()
                    break  # 录音结束后退出循环
            except Exception as e:
                print(e)
                break
        # 获得当前时间戳
        timestamp = str(int(round(time.time() * 1000)))
        # 保存录音文件的路径
        full_audio_path = os.path.join(current_dir_path, "record", f"{timestamp}.wav")
        save_recording(audio_data, full_audio_path)
        audio_path = folder_paths.get_annotated_filepath(full_audio_path)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (
            full_audio_path,
            audio_out,
        )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


class openai_whisper:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "audio_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
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

    def whisper(self,audio_path,is_enable=True,  base_url=None, api_key=None, audio=None):
        if is_enable == False:
            return (None,)
        if api_key != "":
            openai.api_key = api_key
        elif config.get("API_KEYS", "openai_api_key") != "":
            openai.api_key = config.get("API_KEYS", "openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            # 如果以/结尾
            if base_url[-1] == "/":
                openai.base_url = base_url
            else:
                openai.base_url = base_url + "/"
        elif config.get("API_KEYS", "base_url") != "":
            openai.base_url = config.get("API_KEYS", "base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")


        client = OpenAI(api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            client = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        if audio is not None:
            # 获得当前时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 保存录音文件的路径
            audio_path = os.path.join(current_dir_path, "record", f"{timestamp}.wav")
            torchaudio.save(audio_path, audio["waveform"].squeeze(0), audio["sample_rate"])
            audio_file = open(audio_path, "rb")
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            out = transcription.text
        elif audio_path != "" and audio_path is not None:
            audio_file = open(audio_path, "rb")
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_path)
            out = transcription.text
        else:
            out = None

        return (out,)

NODE_CLASS_MAPPINGS = {
    "listen_audio": listen_audio,
    "openai_whisper": openai_whisper,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import os
import sys


try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "listen_audio": "☁️监听音频",
        "openai_whisper": "☁️OpenAI语音识别",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "listen_audio": "☁️Listen Audio",
        "openai_whisper": "☁️OpenAI ASR",
    }