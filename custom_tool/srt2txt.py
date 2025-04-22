import locale
import srt
import json
import os
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_dir_path = os.path.join(current_dir_path, 'output')
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)
def load_srt(file_path):
    """
    读取SRT文件并提取文本内容和时间戳

    参数:
    file_path (str): SRT文件的路径

    返回:
    tuple: 包含文本内容的列表和时间戳的列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        subs = list(srt.parse(f.read()))

    texts = [sub.content for sub in subs]
    timestamps = [(sub.start, sub.end) for sub in subs]

    return texts, timestamps

def save_translated_srt(translated_texts, timestamps, output_path, file_name='out.srt'):
    """
    保存翻译后的文本为SRT文件

    参数:
    translated_texts (list): 翻译后的文本内容列表
    timestamps (list): 时间戳列表，包含(start, end)元组
    output_dir_path (str): 输出目录路径
    file_name (str): 输出文件名，默认为'out.srt'

    返回:
    None
    """
    # 创建新的字幕对象
    new_subs = []
    for i, (start, end) in enumerate(timestamps):
        sub = srt.Subtitle(index=i+1, start=start, end=end, content=translated_texts[i])
        new_subs.append(sub)

    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)
    
    # 保存为新的SRT文件
    output_path = os.path.join(output_path, file_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(new_subs))


class srt2txt:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"srt_path": ("STRING", {"default": "example.srt"})}}

    RETURN_TYPES = ("STRING","TIMESTAMP")
    RETURN_NAMES = ("texts","timestamps")

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def convert_txt2json(self, srt_path):
        texts, timestamps=load_srt(srt_path)
        texts=json.dumps(texts, ensure_ascii=False, indent=4)
        return (texts, timestamps,)
    
class txt2srt:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "translated_texts": ("STRING", {"forceInput": True}),
            "timestamps": ("TIMESTAMP", {"forceInput": True}),
            "output_dir_path": ("STRING", {"default": output_dir_path}),
            }}

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"
    OUTPUT_NODE = True
    def convert_txt2json(self, translated_texts, timestamps, output_dir_path):
        translated_texts=json.loads(translated_texts)
        save_translated_srt(translated_texts, timestamps, output_dir_path)
        return ()

NODE_CLASS_MAPPINGS = {"srt2txt": srt2txt,"txt2srt": txt2srt}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"srt2txt": "字幕SRT转文本", "txt2srt": "文本转字幕SRT"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"srt2txt": "subtitles SRT to Text", "txt2srt": "Text to subtitles SRT"}