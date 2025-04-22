import numpy as np
import librosa
import torchaudio
import ffmpeg
import locale
import os
import configparser
import torch
from datetime import datetime


def load_audio(path):
    audio, sr = librosa.load(path, sr=None)
    audio = (audio * 32768).astype(np.int16)
    return audio, sr


def speed_change(input_audio: np.ndarray, speed: float, sr: int):
    raw_audio = input_audio.astype(np.int16).tobytes()
    input_stream = ffmpeg.input('pipe:', format='s16le', acodec='pcm_s16le', ar=str(sr), ac=1)
    output_stream = input_stream.filter('atempo', speed)
    out, _ = (
        output_stream.output('pipe:', format='s16le', acodec='pcm_s16le')
        .run(input=raw_audio, capture_stdout=True, capture_stderr=True)
    )
    processed_audio = np.frombuffer(out, np.int16)
    return processed_audio


class SpeedChange:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_audio_path": ("STRING", {}),
                "output_folder_path": ("STRING", {}),
                "speed_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "step": 0.1}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "suffix": ("STRING", {"default": "_processed"}),
            }
        }
    
    RETURN_TYPES = ("AUDIO","STRING",)
    RETURN_NAMES = ("audio","audio_path",)

    FUNCTION = "audio_process"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/音频（audio）"


    def audio_process(self, input_audio_path, output_folder_path, speed_factor, is_enable,suffix):
        if not is_enable:
            return (None, None,)
        
        audio_data, original_sr = load_audio(input_audio_path)
        # 获取input_audio_path的文件名
        filename = os.path.basename(input_audio_path)
        # 获取文件名和扩展名
        filename_without_extension, extension = os.path.splitext(filename)
        processed_audio = speed_change(audio_data, speed_factor, original_sr)
        
        if isinstance(processed_audio, np.ndarray):
            processed_audio = torch.tensor(processed_audio)

        if processed_audio.ndim == 1:
            processed_audio = processed_audio.unsqueeze(0)

        output_audio_filename = f"{filename_without_extension}_{suffix}{extension}"
        output_audio_path = os.path.join(output_folder_path, output_audio_filename)
        torchaudio.save(output_audio_path, processed_audio, original_sr)
        
        waveform, sample_rate = torchaudio.load(output_audio_path)
        audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (audio_out, output_audio_path,)
        

NODE_CLASS_MAPPINGS = {"SpeedChange": SpeedChange}

lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"SpeedChange": "音频变速🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"SpeedChange": "AudioSpeedChange🐶"}

if __name__ == "__main__":
    audio_file_paths = r'E:\ComfyUI\custom_nodes\comfyui_LLM_party\custom_tool\output\20240912212300.wav'
    speed_factor = 0.7
    output_file_path = r'E:\ComfyUI\custom_nodes\comfyui_LLM_party\custom_tool\output'

    obj = SpeedChange()
    obj.audio_process(audio_file_paths, output_file_path, speed_factor, True)
