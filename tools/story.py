import json
import os

from ..config import current_dir_path

file_path = os.path.join(current_dir_path, "file")

story_path = ""


class story_json_tool:
    @classmethod
    def INPUT_TYPES(s):
        # 获取file_path文件夹下的所有json文件的文件名
        paths = [f for f in os.listdir(file_path) if f.endswith(".json")]
        return {
            "required": {
                "path": (paths, {"default": "story.json"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, path, is_enable=True):
        if is_enable == False:
            return (None,)
        path = os.path.join(file_path, path)
        global story_path
        story_path = path
        output = [
            {
                "type": "function",
                "function": {
                    "name": "read_story_json",
                    "description": "用于查询小说对应章节的内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chapter": {
                                "type": "string",
                                "description": "章节的数目，例如：0, 5, 1-1, 2-2-1, 3-23-42-12",
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
    out = json.dumps(data[str(chapter)], ensure_ascii=False, indent=4)
    return out
