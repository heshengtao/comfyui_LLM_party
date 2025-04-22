import json
import feedparser
import locale

class RSS_loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "rss_url": ("STRING", {"default":"https://feeds.bbci.co.uk/news/world/rss.xml"}), 
                "is_enable": ("BOOLEAN", {"default": True}),
                }
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_str",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def convert_txt2json(self, rss_url, is_enable=True):
        if is_enable == False:
            return (None,)
        # 解析RSS链接
        feed = feedparser.parse(rss_url)

        # 创建一个字典来存储RSS Feed的信息
        rss_data = {
            "feed_title": feed.feed.title,
            "entries": []
        }

        # 遍历并添加每个条目的信息到字典中
        for entry in feed.entries:
            rss_data["entries"].append({
                "title": entry.get("title", "No Title"),
                "link": entry.get("link", "No Link"),
                "published": entry.get("published", "No Published Date"),
                "summary": entry.get("summary", "No Summary")
            })
        # 将字典转换为JSON字符串
        json_str = json.dumps(rss_data, ensure_ascii=False, indent=4)
        return (json_str,)
    
def rss_get(rss_url):
    # 解析RSS链接
    feed = feedparser.parse(rss_url)

    # 创建一个字典来存储RSS Feed的信息
    rss_data = {
        "feed_title": feed.feed.title,
        "entries": []
    }

    # 遍历并添加每个条目的信息到字典中
    for entry in feed.entries:
        rss_data["entries"].append({
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", "No Link"),
            "published": entry.get("published", "No Published Date"),
            "summary": entry.get("summary", "No Summary")
        })
    # 将字典转换为JSON字符串
    json_str = json.dumps(rss_data, ensure_ascii=False, indent=4)
    return json_str

class RSS_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                }
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def convert_txt2json(self, is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "rss_get",
                    "description": "查询解析RSS，返回json格式数据",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rss_url": {"type": "string", "description": "要查询的RSS地址"},
                        },
                        "required": ["rss_url"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
    
_TOOL_HOOKS = ["rss_get"]
NODE_CLASS_MAPPINGS = {
    "RSS_loader": RSS_loader,
    "RSS_tool": RSS_tool,
    }
# 获取系统语言
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
    NODE_DISPLAY_NAME_MAPPINGS = {
        "RSS_loader": "RSS加载器",
        "RSS_tool": "RSS工具",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "RSS_loader": "RSS Loader",
        "RSS_tool": "RSS Tool",}