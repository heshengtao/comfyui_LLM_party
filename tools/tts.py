import io
import os
import shutil
import time

import openai
import requests
if os.name == 'nt':
    import winsound
else:
    from playsound import playsound

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
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    FUNCTION = "tts"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def tts(self, is_enable=True, input_string="", base_url=None, api_key=None, model_name="tts-1", voice="alloy"):
        if is_enable == False:
            return (None,)

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
            return ("请输入API_KEY",)

        if input_string != "":
            # 获得当前时间戳
            timestamp = str(int(round(time.time() * 1000)))
            # 判断当前目录是否存在audio文件夹，如果不存在则创建
            if not os.path.exists(os.path.join(current_dir_path, "audio")):
                os.makedirs(os.path.join(current_dir_path, "audio"))
            full_audio_path = os.path.join(current_dir_path, "audio", f"{timestamp}.mp3")
            # 请将'your_openai_api_key'替换为您的OpenAI API密钥
            openai_api_key = openai.api_key
            # 定义基础URL
            base_url = openai.base_url

            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json",
            }

            data = {"model": model_name, "input": input_string, "voice": voice}

            # 使用base_url变量构建完整的URL
            response = requests.post(f"{base_url}audio/speech", headers=headers, json=data)
            # 将响应内容写入MP3文件
            with open(full_audio_path, "wb") as f:
                f.write(response.content)

            out = full_audio_path
        else:
            out = None
        return (out,)


class play_audio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO", {}),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    FUNCTION = "tts"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def tts(self, audio):
        # 判断当前目录是否存在audio文件夹，如果不存在则创建
        if not os.path.exists(os.path.join(current_dir_path, "audio")):
            os.makedirs(os.path.join(current_dir_path, "audio"))
        # 如果这个audio音频不在audio文件夹下，剪切这个文件到audio文件夹下，然后播放这个音频
        if not os.path.dirname(audio) == os.path.join(current_dir_path, "audio"):
            shutil.move(audio, os.path.join(current_dir_path, "audio", os.path.basename(audio)))
            audio = os.path.join(current_dir_path, "audio", os.path.basename(audio))
        # 播放音频文件
        audio = os.path.normpath(audio)
        print("[playsound]:", audio)
        if os.name == 'nt':
            winsound.PlaySound(audio, winsound.SND_FILENAME)
        else:
            playsound(audio)
                        

        return ()
