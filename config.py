# 获取当前文件的绝对路径
import configparser
import os

current_file_path = os.path.abspath(__file__)

# 获取当前文件所在目录的路径
current_dir_path = os.path.dirname(current_file_path)

# 构建config.ini的绝对路径
config_path = os.path.join(current_dir_path, "config.ini")


def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys
