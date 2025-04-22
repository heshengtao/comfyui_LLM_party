import locale
import hashlib
import os

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import json
import datetime
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
Base = declarative_base()

class Dialogue(Base):
    __tablename__ = 'dialogue_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(50))
    content = Column(Text)

class load_SQL_memo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "history_id": ("INT", {"default": 1}),  # 假设每个对话有一个唯一ID
                "database_url": ("STRING", {"default": "postgresql://myuser:mypassword@localhost:5432/mydatabase"}),
                "clear_memo": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "INT",
    )
    RETURN_NAMES = (
        "system_prompt",
        "user_history",
        "history_id",
    )

    FUNCTION = "memo"

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self, database_url, system_prompt="", history_id=1, clear_memo=False):
        # 创建数据库引擎和会话
        engine = create_engine(database_url)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()

        try:
            # 创建表（如果不存在）
            Base.metadata.create_all(engine)

            # 检查是否需要清空历史记录
            if clear_memo:
                with session.no_autoflush:
                    session.query(Dialogue).delete()
                    session.commit()

            # 检查数据库是否为空
            history_records = session.query(Dialogue).order_by(Dialogue.id).all()
            
            # 构建历史记录列表
            history_list = []
            
            # 如果没有系统提示或需要更新系统提示
            system_exists = any(record.role == "system" for record in history_records)
            if not system_exists or (system_prompt and system_exists):
                # 如果已存在系统提示且有新的系统提示，更新它
                if system_exists and system_prompt:
                    for record in history_records:
                        if record.role == "system":
                            record.content = system_prompt
                            session.commit()
                            break
                # 如果不存在系统提示且有新的系统提示，添加它
                elif system_prompt:
                    system_record = Dialogue(role="system", content=system_prompt)
                    session.add(system_record)
                    session.commit()
                    history_records = [system_record] + history_records

            # 构建包含所有历史记录的字符串
            known_info = "\n".join([f"{record.role}: {record.content}" for record in history_records])
            
            # 创建历史记录列表，确保系统提示在第一位
            for record in history_records:
                message = {
                    "role": record.role,
                    "content": record.content
                }
                if record.role == "system":
                    # 为系统消息添加已知信息
                    message["content"] = f"{record.content}\n以下是可以参考的已知信息:\n{known_info}"
                    history_list.insert(0, message)  # 系统消息始终放在第一位
                else:
                    history_list.append(message)

            # 如果没有系统提示但需要返回历史记录
            if not any(msg["role"] == "system" for msg in history_list):
                history_list.insert(0, {
                    "role": "system",
                    "content": f"你是我的恋人\n以下是可以参考的已知信息:\n{known_info}"
                })

            user_history = json.dumps(history_list, ensure_ascii=False, indent=4)
            
            return (
                system_prompt,
                user_history,
                history_id,
            )
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def IS_CHANGED(cls):
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

class save_SQL_memo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "history": ("STRING", {"forceInput": True}),
                "history_id": ("INT", {"forceInput": True}),
                "database_url": ("STRING", {"default": "postgresql://myuser:mypassword@localhost:5432/mydatabase"}),
            },
        }

    RETURN_TYPES = (
        "INT",
    )
    RETURN_NAMES = (
        "history_id",
    )

    FUNCTION = "memo"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self, history, history_id, database_url):
        # 创建数据库引擎和会话
        engine = create_engine(database_url)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()

        try:
            # 将历史记录字符串转换为列表
            history_list = json.loads(history)

            # 获取现有系统提示
            system_record = session.query(Dialogue).filter_by(role="system").first()
            if not system_record:
                # 如果没有系统提示，创建默认系统提示
                system_record = Dialogue(role="system", content="你是我的恋人")
                session.add(system_record)

            # 删除现有的非系统提示记录
            session.query(Dialogue).filter(Dialogue.role != "system").delete()

            # 插入新的对话记录
            for message in history_list:
                if message['role'] != 'system':  # 不重复插入系统提示
                    new_record = Dialogue(
                        role=message['role'],
                        content=message['content']
                    )
                    session.add(new_record)

            session.commit()

        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

        return (history_id,)

    @classmethod
    def IS_CHANGED(cls):
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

NODE_CLASS_MAPPINGS = {
    "load_SQL_memo": load_SQL_memo,
    "save_SQL_memo": save_SQL_memo,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'

try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_SQL_memo": "加载SQL记忆",
        "save_SQL_memo": "保存SQL记忆",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_SQL_memo": "load SQL memory",
        "save_SQL_memo": "save SQL memory",
    }
