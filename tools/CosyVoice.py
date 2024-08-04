from gradio_client import Client
import folder_paths
import torchaudio

def CosyVoice_audio(text, voice="中文女", voice_seed=1, api_name="/generate_audio"):
    client = Client("https://s5k.cn/api/v1/studio/iic/CosyVoice-300M/gradio/")
    result = client.predict(_sound_radio=voice, _synthetic_input_textbox=text, _seed=voice_seed, api_name=api_name)
    return result


class CosyVoice:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "text": ("STRING", {"default": "你好，我是大模型派对"}),
                "seed": ("INT", {"default": 1, "min": 1, "max": 100000000}),
                "api_name": (
                    ["/generate_audio", "/generate_audio_1", "/generate_audio_2"],
                    {"default": "/generate_audio"},
                ),
                "voice": (
                    ["中文女", "中文男", "英文女", "英文男", "日语男", "粤语女", "韩语女"],
                    {"default": "中文女"},
                ),
            },
        }

    RETURN_TYPES = ("STRING","AUDIO",)
    RETURN_NAMES = ("audio_path","audio",)

    FUNCTION = "tts"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def tts(self, is_enable=True, text="你好，我是大模型派对", seed=1, api_name="/generate_audio", voice="中文女"):
        if is_enable == False:
            return (None,)
        if text == "":
            return (None,)
        out = CosyVoice_audio(text, voice, seed, api_name)
        audio_path = folder_paths.get_annotated_filepath(out)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (out,audio_out,)
