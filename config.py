# 获取当前文件的绝对路径
import configparser
import os
import shutil

current_file_path = os.path.abspath(__file__)

# 获取当前文件所在目录的路径
current_dir_path = os.path.dirname(current_file_path)

# 构建config.ini的绝对路径
config_path = os.path.join(current_dir_path, "config.ini")


def copy_config():
    config_path = os.path.join(current_dir_path, "config.ini")
    config_example_path = os.path.join(current_dir_path, "config.ini.example")
    # 判断config.ini是否存在
    if not os.path.exists(config_path):
        # 如果不存在用config_example_path的副本创建config.ini
        shutil.copyfile(config_example_path, config_path)


copy_config()
config_key = configparser.ConfigParser()
config_key.read(config_path, encoding="utf-8")
# 获取config_key中的API_KEYS部分
api_keys = config_key["API_KEYS"]


# 获取config_key中的所有部分
config_keys = config_key.sections()
# 删除config_key中名为"API_KEYS"的元素
del config_keys[config_keys.index("API_KEYS")]


def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys