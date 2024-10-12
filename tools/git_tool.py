import json
from datetime import date

import requests

from ..config import config_path, load_api_keys

# 加载API密钥的函数保持不变
api_keys = load_api_keys(config_path)
github_api_key = api_keys.get("github_api_key")


def search_github_repositories(keywords, paper_num, url=None):
    today = str(date.today())
    global github_api_key
    num_results = 10
    start = num_results * (int(paper_num) - 1)
    try:
        # 使用GitHub API的基础URL
        base_url = "https://api.github.com/search/repositories"
        headers = {"Authorization": f"token {github_api_key}"}
        params = {
            "q": keywords if isinstance(keywords, str) else " ".join(keywords),
            "sort": "stars",
            "order": "desc",
            "per_page": num_results,
            "page": paper_num,
        }

        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        # 打印HTTP状态码和响应内容以供调试
        print("Status code:", response.status_code)
        print("Response body:", response.text)

        all_content = ""
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                repo_name = item["full_name"]
                repo_url = item["html_url"]
                all_content += json.dumps({"repo_name": repo_name, "repo_url": repo_url}, ensure_ascii=False, indent=4)

        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred: {e}"

    print(all_content)
    return (
        "今天的日期是"
        + today
        + "，当前GitHub上的仓库信息和信息来源的网址为：“"
        + str(all_content)
        + "”。\n如果以上信息中没有相关信息，你可以改变paper_num，查看下一页的信息。"
    )


# 类定义和方法保持不变，只需将bing_tool更名为github_tool，并更新相关注释
class github_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "git_api_key": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def web(self, git_api_key=None, is_enable=True):
        if is_enable == False:
            return (None,)
        global github_api_key
        if git_api_key is not None and git_api_key != "":
            github_api_key = git_api_key
        else:
            github_api_key = api_keys.get("github_api_key")
        output = [
            {
                "type": "function",
                "function": {
                    "name": "search_github_repositories",
                    "description": "通过关键词获得GitHub上的仓库信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "string",
                                "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开",
                            },
                            "paper_num": {
                                "type": "string",
                                "description": "GitHub搜索的页码，可以改变paper_num用于翻页",
                            },
                        },
                        "required": ["keywords", "paper_num"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)
