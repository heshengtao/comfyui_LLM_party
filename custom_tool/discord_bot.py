import json
import locale
import os
import subprocess
import sys
import time
import discord
from discord.ext import commands
current_dir = os.path.dirname(os.path.abspath(__file__))
discord_temp_dir = os.path.join(current_dir, 'discord_temp')
discord_send_dir = os.path.join(current_dir, 'discord_send')
# 清空discord_temp_dir目录下的文件




class discord_bot:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "token": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "function_name": ("STRING", {"default": '["ping", "add"]'}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "bot"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def bot(self, token, function_name='["ping", "add"]', is_enable=True):
        if not is_enable:
            return ()
        
        function_name = json.loads(function_name)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        run_bot_code = os.path.join(current_dir, 'run_bot.py')

        # 创建一个新的 Python 文件来运行 bot
        with open(run_bot_code, "w", encoding='utf-8') as f:
            f.write(f"""
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
from discord import Attachment
import json
import os
import time
import asyncio
                    
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def synccommands(ctx):
    await bot.tree.sync()
    await ctx.send("Commands synced")

# 保存输入到 JSON 文件的函数
async def save_input(command, type, input, timestamp):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    discord_temp_dir = os.path.join(current_dir, 'discord_temp')
    os.makedirs(discord_temp_dir, exist_ok=True)
    file_path = os.path.join(discord_temp_dir, f"{{timestamp}}.json")
    
    # 如果文件存在，读取现有内容
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    # 添加新的输入到字典列表中
    data.append({{command:input}})
    
    # 写入更新后的内容到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        

def read_res():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    discord_send_dir = os.path.join(current_dir, 'discord_send')
    os.makedirs(discord_send_dir, exist_ok=True)
    while True:
        files = os.listdir(discord_send_dir)
        json_files = [f for f in files if f.endswith('.json')]
        if json_files:
            earliest_file = min(json_files, key=lambda f: os.path.getctime(os.path.join(discord_send_dir, f)))
            file_path = os.path.join(discord_send_dir, earliest_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
            os.remove(file_path)
            text = content.get('text')
            image = content.get('image')
            audio = content.get('audio')
            return text, image, audio

@tasks.loop(count=1)
async def process_task(ctx):
    text, image, audio = read_res()
    if text is not None:
        await ctx.send(text)
    if image is not None:
        await ctx.send(file=discord.File(image))
    if audio is not None:
        await ctx.send(file=discord.File(audio))                   

# 动态生成命令函数
""")
            for command in function_name:
                f.write(f"""
@bot.hybrid_command()
async def {command}(ctx, text1: str = None, text2: str = None, file1: Attachment = None, file2: Attachment = None):
    timestamp = int(time.time())
    inputs = [text1, text2]
    attachments = [file1, file2]

    # 如果 text1 和 text2 都为空，则使用用户输入的完整消息内容
    if not any(inputs):
        inputs = [ctx.message.content.replace(f'!{{ctx.command}}', '').strip()]    

    for input in inputs:
        if input:
            await save_input("{command}", "text", input, timestamp)
        else:
            await save_input("{command}", "text", "", timestamp)
    
    for attachment in attachments:
        if attachment:
            await save_input("{command}", "image", attachment.url, timestamp)
        else:
            await save_input("{command}", "image", "", timestamp)
    
    if not any(inputs) and not any(attachments):
        await ctx.send("Please provide either text or an image.")

    await ctx.send(f"Thinking about ...")
    process_task.start(ctx)
""")
            
            f.write(f"""
if __name__ == "__main__":
    bot.run("{token}")
""")

        # 根据操作系统选择打开终端的命令
        if sys.platform == "win32":
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            subprocess.Popen(["start", "cmd", "/k", sys.executable, run_bot_code], shell=True, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", "-a", "Terminal", sys.executable, run_bot_code], start_new_session=True)
        else:  # Linux
            try:
                subprocess.Popen(["screen", "-dmS", "bot_session", sys.executable, run_bot_code], start_new_session=True)
            except FileNotFoundError:
                try:
                    subprocess.Popen(["tmux", "new-session", "-d", sys.executable, run_bot_code], start_new_session=True)
                except FileNotFoundError:
                    print("No compatible terminal multiplexer found. Please install screen or tmux.")
        
        return ()
    

class discord_send:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "text": ("STRING", {"default": ""}),
                "img_path": ("STRING", {"default": ""}),
                "audio_path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "bot"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def bot(self,text,img_path,audio_path, is_enable=True):    
        if not is_enable:
            return ()
        timestamp = int(time.time())
        msg={}
        # 将文字、图片、音频保存到discord_send文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        discord_send_dir = os.path.join(current_dir, 'discord_send')
        os.makedirs(discord_send_dir, exist_ok=True)
        if text!="" and text is not None:
            # 把文字信息传入msg["text"]
            msg["text"]=text
        if img_path!="" and text is not None:
            msg["image"]=img_path
        if audio_path!="" and text is not None:
            msg["audio"]=audio_path
        with open(f"{discord_send_dir}/{timestamp}.json", "w", encoding='utf-8') as f:
            json.dump(msg, f, ensure_ascii=False, indent=4)
        return ()


NODE_CLASS_MAPPINGS = {
    "discord_bot": discord_bot,
    "discord_send": discord_send,
    }
lang = locale.getdefaultlocale()[0]
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "discord_bot": "启动discord机器人",
        "discord_send": "发送消息到discord"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "discord_bot": "Start Discord Bot",
        "discord_send": "Send Message to Discord"
    }
