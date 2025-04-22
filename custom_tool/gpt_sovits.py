import locale
import re
import time
import requests
import os
import folder_paths
import torchaudio
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 使用 POST 方法调用 TTS 接口的函数
def post_tts(data):
    url = "http://127.0.0.1:9880/tts"
    headers = {
        'Connection': 'close'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content  # 返回音频流
    else:
        return response.json()  # 返回错误信息

# 控制服务器的函数
def control_server(command):
    url = "http://127.0.0.1:9880/control"
    params = {"command": command}
    response = requests.get(url, params=params)
    return response.status_code

# 设置 GPT 权重的函数
def set_gpt_weights(weights_path):
    url = "http://127.0.0.1:9880/set_gpt_weights"
    params = {"weights_path": weights_path}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return "success"
    else:
        return response.json()  # 返回错误信息

# 设置 Sovits 权重的函数
def set_sovits_weights(weights_path):
    url = "http://127.0.0.1:9880/set_sovits_weights"
    params = {"weights_path": weights_path}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return "success"
    else:
        return response.json()  # 返回错误信息
    



class gpt_sovits:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。"}),
                "text_lang": (["auto", "auto_yue", "en", "zh", "ja", "yue", "ko", "all_zh", "all_ja", "all_yue", "all_ko"], {"default": "zh"}),
                "ref_audio_path": ("STRING", {"default": ""}),
                "prompt_text": ("STRING", {"default": ""}),
                "prompt_lang": (["auto", "en", "zh", "ja", "yue", "ko", "all_zh", "all_ja", "all_yue", "all_ko"], {"default": "zh"}),
                "text_split_method": (["cut0", "cut1", "cut2", "cut3", "cut4", "cut5"], {"default": "cut5"}),
                "batch_size": ("INT", {"default": 1}),
                "media_type": (["wav", "raw", "ogg", "aac"], {"default": "wav"}),
                "GPT_weights_path": ("STRING", {"default": ""}),
                "Sovits_weights_path": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("AUDIO","STRING",)
    RETURN_NAMES = ("audio","audio_path",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/音频（audio）"

    def time(self, text,text_lang, ref_audio_path, prompt_text, prompt_lang, text_split_method, batch_size, media_type,GPT_weights_path="", Sovits_weights_path="", is_enable=True):
        if is_enable == False:
            return (None,)
        if GPT_weights_path != "":
            set_gpt_weights(GPT_weights_path)
        if Sovits_weights_path != "":
            set_sovits_weights(Sovits_weights_path)
        # 如果text_lang=zh,删除text中所有的非中文字符（包含英文标点，不包含中文标点）
        if text_lang == "zh":
            text = re.sub(r'[^\u4e00-\u9fa5，。！？；：、（）《》“”‘’]', '', text)
        data = {
    "text": text,
    "text_lang": text_lang,
    "ref_audio_path": ref_audio_path,
    "prompt_text": prompt_text,
    "prompt_lang": prompt_lang,
    "text_split_method": text_split_method,
    "batch_size": batch_size,
    "media_type": media_type,
    "streaming_mode": False,
}
        audio_stream = post_tts(data)
        # 如果audio_stream是一个字典
        if isinstance(audio_stream, dict):
            print("audio_stream is a dict:", audio_stream)
        # 判断当前目录是否存在audio文件夹，如果不存在则创建
        if not os.path.exists(os.path.join(current_dir_path, "audio")):
            os.makedirs(os.path.join(current_dir_path, "audio"))
        timestamp = int(time.time() * 1000)
        full_audio_path = os.path.join(current_dir_path, "audio", f"{timestamp}.{media_type}")
        with open(full_audio_path, "wb") as f:
            f.write(audio_stream)
        out = full_audio_path
        audio_path = folder_paths.get_annotated_filepath(out)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (audio_out,audio_path,)
        


NODE_CLASS_MAPPINGS = {"gpt_sovits": gpt_sovits}
# 获取系统语言
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
    NODE_DISPLAY_NAME_MAPPINGS = {"gpt_sovits": "🖥️GPT-SoVITS"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"gpt_sovits": "🖥️GPT-SoVITS"}