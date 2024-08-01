# 当前脚本目录
import datetime
import hashlib
import json
import locale
import os
import time


current_dir = os.path.dirname(os.path.abspath(__file__))
discord_temp_dir = os.path.join(current_dir, 'discord_temp')
os.makedirs(discord_temp_dir, exist_ok=True)
for file in os.listdir(discord_temp_dir): os.remove(os.path.join(discord_temp_dir, file))
class discord_file_monitor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "interval":("FLOAT",{"default":0.1}),
            }
        }

    RETURN_TYPES = (
        "STRING",
    )
    RETURN_NAMES = (
        "msg_content",
    )

    FUNCTION = "monitor"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def monitor(self, interval=0.1):
        show_help = "placeholder for help text"
        while True:
            # 获取feishu_temp_dir目录下的所有文件
            files = os.listdir(discord_temp_dir)
            # 过滤出JSON文件
            json_files = [f for f in files if f.endswith('.json')]
            if json_files:
                # 找到最早的JSON文件
                earliest_file = min(json_files, key=lambda f: os.path.getctime(os.path.join(discord_temp_dir, f)))
                file_path = os.path.join(discord_temp_dir, earliest_file)
                # 读取文件内容并转换为字符串
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                # 删除文件
                os.remove(file_path)
                msg_content= json.dumps(content, ensure_ascii=False,indent=4)
                return (
                    msg_content,
                )
            else:
                pass
            # 等待一段时间后再次检查
            time.sleep(interval)
    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value            



NODE_CLASS_MAPPINGS = {"discord_file_monitor": discord_file_monitor}
lang = locale.getdefaultlocale()[0]
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "discord_file_monitor": "discord文件夹监听节点"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "discord_file_monitor": "Discord File Monitor Node"
    }
