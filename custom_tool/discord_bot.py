import json
import locale
import os
import subprocess
import sys
import time

import discord
from discord.ext import commands

current_dir = os.path.dirname(os.path.abspath(__file__))
discord_temp_dir = os.path.join(current_dir, "discord_temp")
discord_send_dir = os.path.join(current_dir, "discord_send")
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

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_success",)

    FUNCTION = "bot"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def bot(self, token, function_name='["ping", "add"]', is_enable=True):
        if not is_enable:
            return ()

        function_name = json.loads(function_name)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        run_bot_code = os.path.join(current_dir, "run_bot.py")

        # 创建一个新的 Python 文件来运行 bot
        with open(run_bot_code, "w", encoding="utf-8") as f:
            f.write(
                f"""
# -*- coding: utf-8 -*-
import discord
from discord.ext import tasks
from discord import Attachment
import json
import os
import time
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

# 保存输入到 JSON 文件的函数
async def save_input(command, input, timestamp):
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


async def read_res():
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
    text, image, audio = await read_res()

    # 处理 text
    if text is not None:
        if isinstance(text, list):
            for t in text:
                await ctx.send(t)
        else:
            await ctx.send(text)

    # 处理 image
    if image is not None:
        if isinstance(image, list):
            for img in image:
                await ctx.send(file=discord.File(img))
        else:
            await ctx.send(file=discord.File(image))

    # 处理 audio
    if audio is not None:
        if isinstance(audio, list):
            for aud in audio:
                await ctx.send(file=discord.File(aud))
        else:
            await ctx.send(file=discord.File(audio))

# 动态生成命令函数
"""
            )
            for command in function_name:
                f.write(
                    f"""
@bot.slash_command()
async def {command}(ctx, text1: str = "", text2: str = "", file1: discord.Attachment = None, file2: discord.Attachment = None):
    await ctx.defer()
    try:
        timestamp = int(time.time())
        inputs = [text1, text2]
        if file1:
            file1 = file1.url
        else:
            file1 = ""
        if file2:
            file2 = file2.url
        else:
            file2 = ""
        attachments = [file1, file2]

        # 如果 text1 和 text2 都为空，则使用用户输入的完整消息内容
        if not any(inputs):
            inputs = [ctx.interaction.data.get('options', [{{}}])[0].get('value', '').strip(), ""]

        for input in inputs:
            if input:
                await save_input(f"{command}", input, timestamp)
            else:
                await save_input(f"{command}", "", timestamp)

        for attachment in attachments:
            if attachment:
                await save_input(f"{command}", attachment, timestamp)
            else:
                await save_input(f"{command}", "", timestamp)

        if not any(inputs) and not any(attachments):
            await ctx.send("Please provide either text or an image.")

        await ctx.send(f"Thinking about ...")
        asyncio.create_task(process_task(ctx, timestamp))
        await ctx.followup.send("Processing complete.")
    except Exception as e:
        print(f"An error occurred: {{e}}")
        await ctx.send("An error occurred while processing your request. Please try again later.")

    finally:
        # 这里可以放置任何需要在无论是否发生异常的情况下都要执行的代码
        print("Command execution completed.")
"""
                )

            f.write(
                f"""
if __name__ == "__main__":
    bot.run("{token}")
"""
            )

        # 根据操作系统选择打开终端的命令
        if sys.platform == "win32":
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            subprocess.Popen(
                ["start", "cmd", "/k", sys.executable, run_bot_code],
                shell=True,
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
            )
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", "-a", "Terminal", sys.executable, run_bot_code], start_new_session=True)
        else:  # Linux
            try:
                subprocess.Popen(
                    ["screen", "-dmS", "bot_session", sys.executable, run_bot_code], start_new_session=True
                )
            except FileNotFoundError:
                try:
                    subprocess.Popen(
                        ["tmux", "new-session", "-d", sys.executable, run_bot_code], start_new_session=True
                    )
                except FileNotFoundError:
                    print("No compatible terminal multiplexer found. Please install screen or tmux.")
        out = True
        return (out,)


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


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

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def bot(self, text, img_path, audio_path, is_enable=True):
        if not is_enable:
            return ()
        timestamp = int(time.time())
        msg = {}
        # 将文字、图片、音频保存到discord_send文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        discord_send_dir = os.path.join(current_dir, "discord_send")
        os.makedirs(discord_send_dir, exist_ok=True)
        if text != "" and text is not None:
            # 把文字信息传入msg["text"]
            msg["text"] = text
        if img_path != "" and text is not None:
            msg["image"] = img_path
        if audio_path != "" and text is not None:
            msg["audio"] = audio_path
        with open(f"{discord_send_dir}/{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(msg, f, ensure_ascii=False, indent=4)
        return ()


NODE_CLASS_MAPPINGS = {
    "discord_bot": discord_bot,
    "discord_send": discord_send,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"discord_bot": "启动discord机器人", "discord_send": "发送消息到discord"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"discord_bot": "Start Discord Bot", "discord_send": "Send Message to Discord"}
