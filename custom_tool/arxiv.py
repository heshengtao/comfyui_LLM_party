import json
import locale

import arxiv


def get_arxiv(query, max_results=3):

    # 创建搜索对象
    search = arxiv.Search(query=query, max_results=int(max_results), sort_by=arxiv.SortCriterion.SubmittedDate)

    # 初始化一个空字符串来存储论文信息
    papers_info = ""
    i = 0
    # 获取前十篇论文的信息
    for result in search.results():
        i += 1
        paper_info = f"{i}:\nDOI: {result.doi or 'N/A'}\nID: {result.entry_id}\nTitle: {result.title}\nAbstract: {result.summary}\nAuthors: {', '.join(author.name for author in result.authors)}\nCategory: {result.primary_category}\nLink: {result.pdf_url}\n\n"
        papers_info += paper_info

    return papers_info


class arxiv_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "query": ("STRING", {"default": "query"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "arxiv"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def arxiv(self, query, is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "get_arxiv",
                    "description": "用于查询arxiv上的最新的相关论文",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "需要查询的关键词，例如：quantum physics",
                                "default": query,
                            },
                            "max_results": {
                                "type": "string",
                                "description": "需要查询的论文数量",
                                "default": "3",
                            },
                        },
                        "required": ["query"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


_TOOL_HOOKS = ["get_arxiv"]
NODE_CLASS_MAPPINGS = {"arxiv_tool": arxiv_tool}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"arxiv_tool": "arxiv工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"arxiv_tool": "arxiv Tool"}
