import io
import os
import shutil
import time

import folder_paths
import openai
import requests
import torchaudio
from openai import OpenAI,AzureOpenAI
from ..config import config_path, current_dir_path, load_api_keys


class openai_tts:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "input_string": ("STRING", {}),
                "model_name": (["tts-1", "tts-1-hd"], {"default": "tts-1"}),
                "voice": (["alloy", "echo", "fable", "onyx", "nova", "shimmer"], {"default": "alloy"}),
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

    def tts(self, is_enable=True, input_string="", base_url=None, api_key=None, model_name="tts-1", voice="alloy"):
        if is_enable == False:
            return (None,)
        audio_out = None
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            # 如果以/结尾
            if base_url[-1] == "/":
                openai.base_url = base_url
            else:
                openai.base_url = base_url + "/"
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")

        if input_string != "":
            # 获得当前时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 判断当前目录是否存在audio文件夹，如果不存在则创建
            if not os.path.exists(os.path.join(current_dir_path, "audio")):
                os.makedirs(os.path.join(current_dir_path, "audio"))
            full_audio_path = os.path.join(current_dir_path, "audio", f"{timestamp}.mp3")

            # 请将'your_openai_api_key'替换为您的OpenAI API密钥
            openai_client = OpenAI(api_key=openai.api_key,base_url=openai.base_url)
            if "openai.azure.com" in openai.base_url:
                # 获取API版本
                api_version = openai.base_url.split("=")[-1].split("/")[0]
                # 获取azure_endpoint
                azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
                openai_client = AzureOpenAI(
                    api_key= openai.api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint,
                )
            # 构建请求数据
            data = {
                "model": model_name,
                "input": input_string,
                "voice": voice
            }

            # 发送POST请求
            response = openai_client.audio.speech.create(
                model=data["model"],
                input=data["input"],
                voice=data["voice"]
            )

            # 将响应内容写入MP3文件
            with open(full_audio_path, "wb") as f:
                f.write(response.content)
            out = full_audio_path
            waveform, sample_rate = torchaudio.load(full_audio_path)
            audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        else:
            out = None
        return (
            out,
            audio_out,
        )
