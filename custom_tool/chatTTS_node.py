import os
import time

import ChatTTS
import jax
import numpy as np
import torch

torch.compile = lambda *args, **kwargs: args[0]
import torchaudio

if os.name == "nt":

    import winsound
else:
    from playsound import playsound


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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio",)
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
        return (full_audio_path,)


NODE_CLASS_MAPPINGS = {
    "ChatTTS_Node": ChatTTS_Node,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ChatTTS_Node": "本地文字转语音🐶（ChatTTS）",
}

if __name__ == "__main__":
    input1 = """
    chat T T S is a text to speech model designed for dialogue applications.
    [uv_break]it supports mixed language input [uv_break]and offers multi speaker
    capabilities with precise control over prosodic elements like
    [uv_break]laughter[uv_break][laugh], [uv_break]pauses, [uv_break]and intonation.
    [uv_break]it delivers natural and expressive speech,[uv_break]so please
    [uv_break] use the project responsibly at your own risk.[uv_break]
    """  # English is still experimental.

    input2 = """
    《乌鸦喝水》（英语：The Crow and the Pitcher，或译为《乌鸦和水壶》）是《伊索寓言》里的一则故事。
    故事描绘了一只乌鸦通过向水壶中投掷小石块而喝到壶中的水。
    现代科学证明，鸦科动物拥有一定的推理和解决问题能力，而非简单的工具性条件反射。
    """

    chat = ChatTTS_Node()
    output = chat.chattts(input1, seed=2048, enableRefine=False)
    print(output)
    # playsound(output[0])
    if os.name == "nt":
        winsound.PlaySound(output[0], winsound.SND_FILENAME)
    output = chat.chattts(input2, seed=2048)
    print(output)
    output = chat.chattts(input1, seed=2048)
