import json
import os

from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine


def query_database(openai_key, db_connection_string, query_str):
    # 设置 OpenAI API 密钥
    os.environ["OPENAI_API_KEY"] = openai_key

    # 创建 PostgreSQL 数据库连接
    engine = create_engine(db_connection_string)

    # 定义 SQL 数据库对象
    sql_database = SQLDatabase(engine)

    # 设置大语言模型
    llm = OpenAI(temperature=0.7, model="gpt-4o")

    # 创建查询引擎
    query_engine = NLSQLTableQueryEngine(sql_database=sql_database, llm=llm)

    # 执行查询
    response = query_engine.query(query_str)

    return response


class db_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "openai_key": ("STRING", {"default": "sk-your-openai-api-key"}),
                "db_connection_string": ("STRING", {"default": "postgresql://user:password@host:port/dbname"}),
                "query_str": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "query_db"

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def query_db(self, openai_key, db_connection_string, query_str, is_enable=True):
        if not is_enable:
            return (None,)

        output = [
            {
                "type": "function",
                "function": {
                    "name": "query_database",
                    "description": "用于执行自然语言查询SQL数据库",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "openai_key": {
                                "type": "string",
                                "description": "OpenAI的API密钥",
                                "default": openai_key,
                            },
                            "db_connection_string": {
                                "type": "string",
                                "description": "PostgreSQL数据库连接字符串",
                                "default": db_connection_string,
                            },
                            "query_str": {
                                "type": "string",
                                "description": "要查询的自然语言查询语句",
                                "default": str(query_str),
                            },
                        },
                        "required": ["openai_key", "db_connection_string", "query_str"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


if __name__ == "__main__":
    print(
        db_tool().query_db(
            "sk-your-openai-api-key",
            "postgresql://fpi4xT8tDYnzwT90H4qJ:FrK6mgLmkC4qFAwZ0FLJ@120.24.88.99:15432/postgres",
            "在2024年5月之前创建的设备有哪些？",
        )
    )
