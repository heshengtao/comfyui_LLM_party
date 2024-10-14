import json
import re
def replace_keys_in_string(s, key_values):
    
    # 使用正则表达式找到所有的 {key} 模式
    keys = re.findall(r'\{(.*?)\}', s)
    # 对找到的每一个键，如果存在于字典中，则替换；否则忽略它
    for key in keys:
        if key in key_values:
            s = s.replace('{' + key + '}', str(key_values[key]))
    return s

class custom_persona:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "根据背景知识，请帮我写一篇关于{主题}的文章。",
                    },
                ),
                "prompt_template": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": '{"主题":"人工智能"}',
                    },
                ),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_or_user_prompt_input",)

    FUNCTION = "custom"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def custom(self, prompt, prompt_template, is_enable=True, file_content=None):
        if is_enable == False:
            return (None,)
        prompt_template=json.loads(prompt_template)
        prompt = replace_keys_in_string(prompt, prompt_template)
        text = ""
        if file_content is not None:
            text = "## 背景知识：\n" + file_content + "\n\n"
        sys_prompt = (
            text
            +
            "## 要求：\n" 
            +
            prompt
        )
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)

