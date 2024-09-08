import inspect
import os
import re
import shutil
from .install import (
    check_and_uninstall_websocket,
    get_system_info,
    init_temp,
    install_llama,
    install_portaudio,
    manage_discord_packages,
)
from .llm import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from server import PromptServer




def get_comfy_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(inspect.getfile(PromptServer))
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def get_web_ext_dir(path):
    dir = get_comfy_dir(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def copy_js_files(ext_path):
    # 设置当前文件夹路径和目标文件夹路径
    current_folder = os.path.dirname(os.path.abspath(__file__))
    target_folder = get_web_ext_dir(ext_path)  # 改为用户目录下的文件夹

    # 确保目标文件夹存在
    try:
        os.makedirs(target_folder, exist_ok=True)
    except PermissionError:
        print(f"没有权限创建目录 {target_folder}")
        return

    # 清空目标文件夹里所有文件
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"无法删除文件 {file_path}: {e}")

    # 获取当前文件夹中web子文件夹下的所有.js文件
    js_files = [f for f in os.listdir(os.path.join(current_folder, "web","js")) if f.endswith(".js")]

    # 复制文件
    for file_name in js_files:
        source_file = os.path.join(current_folder, "web","js", file_name)
        target_file = os.path.join(target_folder, file_name)
        try:
            shutil.copy2(source_file, target_file)
        except Exception as e:
            print(f"无法复制文件 {source_file} 到 {target_file}: {e}")


def get_latest_version_folder(directory):
    version_pattern = re.compile(r'(\d+\.\d+\.\d+)')
    latest_version = None
    latest_folder = None

    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            match = version_pattern.search(folder_name)
            if match:
                version = match.group(1)
                if latest_version is None or version > latest_version:
                    latest_version = version
                    latest_folder = folder_path

    return latest_folder


try:
    install_portaudio()
except Exception as e:
    print(f"Error: {e}")
try:
    dir = get_comfy_dir("web_custom_versions/Comfy-Org_ComfyUI_frontend")
    if os.path.exists(dir):
        latest_folder = get_latest_version_folder(dir)
        party_path= os.path.join(latest_folder,"extensions", "party")
        copy_js_files(party_path)
    copy_js_files("web/extensions/party")
except Exception as e:
    print(f"Error: {e}")
try:
    system_info = get_system_info()
    install_llama(system_info)
except Exception as e:
    print(f"Error: {e}")
try:
    check_and_uninstall_websocket()
except Exception as e:
    print(f"Error: {e}")
try:
    init_temp()
except Exception as e:
    print(f"Error: {e}")
try:
    manage_discord_packages()
except Exception as e:
    print(f"Error: {e}")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
