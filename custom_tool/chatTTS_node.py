import locale
import os
import time

import ChatTTS
import jax
import numpy as np
import torch

torch.compile = lambda *args, **kwargs: args[0]
import torchaudio
import folder_paths
import torchaudio


def deterministic(seed=0):
    """
    Set random seed for reproducibility
    :param seed:
    :return:
    """
    # ref: https://github.com/Jackiexiao/ChatTTS-api-ui-docker/blob/main/api.py#L27
    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class ChatTTS_Node:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {}),
                "model_path": ("STRING", {}),
                "save_path": ("STRING", {}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0}),
                "top_P": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0}),
                "top_K": ("INT", {"default": 20, "min": 0, "max": 100}),
                "enableRefine": ("BOOLEAN", {"default": False}),
                "oral_param": ("INT", {"default": 1, "min": 0, "max": 9}),
                "laugh_param": ("INT", {"default": 0, "min": 0, "max": 2}),
                "break_param": ("INT", {"default": 2, "min": 0, "max": 7}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "load_mode": (["HF", "custom", "local"], {"default": "HF"}),
            },
        }

    RETURN_TYPES = ("STRING","AUDIO",)
    RETURN_NAMES = ("audio_path","audio",)
    FUNCTION = "chattts"
    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def chattts(
        self,
        text,
        seed,
        model_path="",
        save_path="",
        temperature=0.3,
        top_P=0.7,
        top_K=20,
        enableRefine=True,
        oral_param=1,
        laugh_param=0,
        break_param=2,
        is_enable=True,
        load_mode="HF",
    ):
        if not is_enable:
            return (None,)

        text = (
            text.replace("\n", "")
            .replace("》", "")
            .replace("《", "")
            .replace("：", "")
            .replace("）", "")
            .replace("（", "")
        )

        chat = ChatTTS.Chat()
        if load_mode == "local":
            chat.load(compile=False)  # Set to True for better performance
        elif load_mode == "custom":
            if model_path == "" or model_path is None:
                model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
                # 如果没有，创建model文件夹
                if not os.path.exists(model_path):
                    os.mkdir(model_path)
            chat.load(source="custom", compile=False, custom_path=model_path)
        elif load_mode == "HF":
            chat.load(source="huggingface", force_redownload=True)

        deterministic(seed)
        rand_spk = chat.sample_random_speaker()
        # print(rand_spk)
        torch.seed()

        params_infer_code = ChatTTS.Chat.InferCodeParams(
            spk_emb=rand_spk,
            temperature=temperature,
            top_P=top_P,
            top_K=top_K,
        )

        # For sentence level manual control.
        if enableRefine:
            params_refine_text = ChatTTS.Chat.RefineTextParams(
                prompt=f"[oral_{oral_param}][laugh_{laugh_param}][break_{break_param}]"
            )
            wavs = chat.infer(text=text, params_refine_text=params_refine_text, params_infer_code=params_infer_code)
        else:
            wavs = chat.infer(text=text, params_infer_code=params_infer_code)

        timestamp = str(int(round(time.time() * 1000)))
        if save_path == "" or save_path is None:
            save_path = os.path.dirname(os.path.dirname(__file__))
        if not os.path.isabs(save_path):
            save_path = os.path.abspath(save_path)
        if not os.path.exists(os.path.join(save_path, "audio")):
            os.mkdir(os.path.join(save_path, "audio"))
        full_audio_path = os.path.join(save_path, "audio", f"seed{seed}_{timestamp}.wav")

        torchaudio.save(full_audio_path, torch.from_numpy(wavs[0]), 24000, format="wav")
        print("[ChatTTS] Saved audio to: ", full_audio_path)
        audio_path = folder_paths.get_annotated_filepath(full_audio_path)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (full_audio_path,audio_out,)


NODE_CLASS_MAPPINGS = {
    "ChatTTS_Node": ChatTTS_Node,
}
lang = locale.getdefaultlocale()[0]
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "ChatTTS_Node": "chatTTS语音合成🐶"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "ChatTTS_Node": "chatTTS Text-to-Speech🐶"
    }

