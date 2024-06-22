import json
import os
from ..config import current_dir_path
file_path = os.path.join(current_dir_path, "file")

story_path=""
class story_json_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "story.json"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "path_type": (["Absolute_Path", "Relative_Path"], {"default": "Relative_Path"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def file(self, path, path_type, is_enable=True):
        if is_enable == False:
            return (None,)
        if path_type == "Absolute_Path":
            path = path
        else:
            path = os.path.join(file_path, path)
        global story_path
        story_path = path
        output = [
            {
                "type": "function",
                "function": {
                    "name": "read_story_json",
                    "description": "用于查询维基百科上的相关内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chapter": {
                                "type": "string",
                                "description": "章节的数目，例如：0, 1, 2, 3",
                            }
                        },
                        "required": ["chapter"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)

def read_story_json(chapter):
    global story_path
    with open(story_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = json.dumps(data[str(chapter)], ensure_ascii=False,indent=4)
    return out