import os
from ..config import current_dir_path


persona_path = os.path.join(current_dir_path, 'persona')
txt_filenames = [os.path.splitext(file)[0] for file in os.listdir(persona_path) if file.endswith('.txt')]
class load_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "persona_name": (txt_filenames, {
                    "default": None
                }),
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                })
            },
            "optional": {

            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt",)

    FUNCTION = "persona"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def persona(self,persona_name,is_enable="enable"):
        if is_enable=="disable":
            return (None,)
        per_path = os.path.join(persona_path, persona_name + '.txt')
        text=""
        with open(per_path, 'r', encoding='utf-8') as f:
            text += f.read()
        return (text,)