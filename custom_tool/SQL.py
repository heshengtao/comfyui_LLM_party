import configparser
import os
import json
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
import openai
from sqlalchemy import create_engine
from llama_index.core.query_engine import NLSQLTableQueryEngine
import locale
# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")


def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys

db_string = ""
global_model_name = ""
def query_database(query_str):
    global db_string,global_model_name
    # 创建 PostgreSQL 数据库连接
    engine = create_engine(db_string)

    # 定义 SQL 数据库对象
    sql_database = SQLDatabase(engine)

    # 设置大语言模型
    llm = OpenAI(temperature=0.7, model=global_model_name,api_key=openai.api_key, base_url=openai.base_url)

    # 创建查询引擎
    query_engine = NLSQLTableQueryEngine(sql_database=sql_database, llm=llm)

    # 执行查询
    response = query_engine.query(query_str)

    return response


class sql_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "db_connection_string": ("STRING", {"default": "postgresql://user:password@host:port/dbname"}),
                "query_str": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini"}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "query_db"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def query_db(self, api_key,base_url,model_name, db_connection_string, query_str, is_enable=True):

        if not is_enable:
            return (None,)
        global db_string,global_model_name
        db_string = db_connection_string
        api_keys = load_api_keys(config_path)
        global_model_name= model_name
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")

        output = [
            {
                "type": "function",
                "function": {
                    "name": "query_database",
                    "description": "用于执行自然语言查询SQL数据库",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query_str": {
                                "type": "string",
                                "description": "要查询的自然语言查询语句，请不要输入SQL语言，这里输入的是自然语言",
                                "default": str(query_str),
                            }
                        },
                        "required": ["query_str"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
_TOOL_HOOKS = ["query_database"]
NODE_CLASS_MAPPINGS = {
    "sql_tool": sql_tool,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
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
        "sql_tool": "☁️SQL工具"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "sql_tool": "☁️SQL tool"
    }
