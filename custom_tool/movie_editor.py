from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from datetime import datetime
import configparser
import locale
import re


def detect_language(text):
    has_chinese = False
    has_english = False
    
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            has_chinese = True
        elif ('\u0041' <= char <= '\u005A') or ('\u0061' <= char <= '\u007A'):
            has_english = True

    return (has_chinese, has_english)
    

def sort_videos_by_timestamp(file_names):
    # 使用正则表达式提取文件名中的时间戳
    def extract_timestamp(filename):
        match = re.search(r'\d{8,}', filename)
        return int(match.group(0)) if match else 0

    return sorted(file_names, key=extract_timestamp)


class Image2Video_party:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio_path": ("STRING", {}),
                "image_path": ("STRING", {}),
                "subtitle": ("STRING", {"default": "Example subtitle --- LLM Party"}),
                "subtitle_size": ("INT", {"default": 50}),
                "font_path": ("STRING", {"default": "***/***.ttf"}),
                "r": ("INT", {"default": 255, "max": 255, "min": 0, "step": 1}),
                "g": ("INT", {"default": 255, "max": 255, "min": 0, "step": 1}),
                "b": ("INT", {"default": 255, "max": 255, "min": 0, "step": 1}),
                "output_path": ("STRING", {}), 
                "is_enable": ("BOOLEAN", {"default": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)

    FUNCTION = "image_to_video"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/视频（video）"

    def image_to_video(self, audio_path, image_path, subtitle, subtitle_size, font_path, r, g, b, output_path, is_enable):
        if not is_enable:
            return (None, None)
        
        audio = AudioFileClip(audio_path)

        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(font_path, subtitle_size)

        max_width = img.width
        max_height = img.height

        has_cn, _ = detect_language(subtitle)
        if not has_cn:
            words = subtitle.split()
        else:
            words = [subtitle[i:i+2] for i in range(0, len(subtitle), 2)]
        
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if draw.textbbox((0, 0), current_line + ' ' + word, font=font)[2] < max_width:
                if has_cn:
                    current_line += word
                else:
                    current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        line_height = draw.textbbox((0, 0), lines[0], font=font)[3]
        line_spacing = int(subtitle_size * 0.05)  # 行间距=字体大小的5%
        total_text_height = sum([line_height + line_spacing for line in lines[:-1]]) + line_height  # 最后一行不需要额外的间距

        bottom_margin = 0.1 * subtitle_size
        y_text = max_height - bottom_margin - total_text_height

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            x_text = (max_width - width) / 2
            draw.text((x_text, y_text), line, fill=(r, g, b), font=font)
            y_text += height + line_spacing
            

        img_np = np.array(img)

        clip_duration = audio.duration
        img_clip = ImageClip(img_np, duration=clip_duration).set_audio(audio)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}.mp4"
        video_path = os.path.join(output_path, filename)
        img_clip.write_videofile(video_path, fps=24)

        return (video_path,)


class Combine_Videos_party:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_folder": ("STRING", {}),
                "output_folder": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)

    FUNCTION = "concatenate_videos"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/视频（video）"

    def concatenate_videos(self, input_folder, output_folder, is_enable):
        if not is_enable:
            return (None,)
        
        if os.path.isfile(input_folder):
            input_folder = os.path.dirname(input_folder)

        video_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
        
        sorted_video_files = sort_videos_by_timestamp(video_files)
        
        clips = [VideoFileClip(f) for f in sorted_video_files]

        final_clip = concatenate_videoclips(clips, method="compose")
        
        # 将拼接后的视频保存到指定的文件路径
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"{timestamp}.mp4"
        video_path = os.path.join(output_folder, output_filename)
        final_clip.write_videofile(video_path)
        return (video_path,)
    

NODE_CLASS_MAPPINGS = {
    "Image2Video_party": Image2Video_party,
    "Combine_Videos_party": Combine_Videos_party
    }

lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Image2Video_party": "静态图片转视频🐶",
        "Combine_Videos_party": "合并视频🐶"
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Image2Video_party": "Image2Video🐶",
        "Combine_Videos_party": "CombineVideos🐶"
        }
