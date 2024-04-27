import os
from ..config import config_path,current_dir_path,load_api_keys,bge_embeddings

class start_dialog:
    def __init__(self):
        self.start = True
        #生成一个hash值作为id
        self.id=hash(str(self))
        # 构建prompt.txt的绝对路径
        self.prompt_path = os.path.join(current_dir_path,"temp", str(self.id)+'.txt')
        # 如果文件不存在，创建prompt.txt文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                f.write('')


    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "start_dialog": ("STRING", {

                })
            }
        }
    
    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("dialog_id","user_prompt",)

    FUNCTION = "dialog"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具和函数（persona&function）"



    def dialog(self, start_dialog):
        if self.start == False:
            # 读取prompt.txt文件内容
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                prompt = f.read()
        else:
            prompt = start_dialog
            self.start = False
        dialog_id=self.id
        return (prompt,dialog_id,)
    
class end_dialog:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dialog_id": ("STRING", {
                    "forceInput": True
                }),
                "assistant_response": ("STRING", {
                    "forceInput": True
                })
            }
        }
    
    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "dialog"

    OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具和函数（persona&function）"



    def dialog(self, dialog_id,assistant_response):
        # 构建prompt.txt的绝对路径
        self.prompt_path = os.path.join(current_dir_path,"temp", str(dialog_id)+'.txt')
        # 如果文件不存在，创建prompt.txt文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                f.write(assistant_response)
        return ()