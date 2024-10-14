import os

from ..config import current_dir_path

persona_path = os.path.join(current_dir_path, "persona")
txt_filenames = [os.path.splitext(file)[0] for file in os.listdir(persona_path) if file.endswith(".txt")]


class load_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "persona_name": (txt_filenames, {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt_input",)

    FUNCTION = "persona"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def persona(self, persona_name, is_enable=True, file_content=None):
        if is_enable == False:
            return (None,)
        per_path = os.path.join(persona_path, persona_name + ".txt")
        text = ""
        if file_content is not None:
            text += "##背景知识：\n" + file_content + "\n\n"
        if os.path.exists(per_path):
            with open(per_path, "r", encoding="utf-8") as f:
                text += f.read()
        return (text,)
