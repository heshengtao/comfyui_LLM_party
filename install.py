import importlib
import os
import platform
import re
import shutil
import subprocess
import sys

import packaging.tags
from requests import get
# 获取当前文件的绝对路径
import configparser
import os
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

def get_python_version():
    """Return the Python version in a concise format, e.g., '39' for Python 3.9."""
    version_match = re.match(r"3\.(\d+)", platform.python_version())
    if version_match:
        return "3" + version_match.group(1)
    else:
        return None


def latest_lamacpp(system_info):
    try:
        response = get("https://api.github.com/repos/abetlen/llama-cpp-python/releases")
        releases = response.json()
        for release in releases:
            tag_name = release["tag_name"].lower()
            if system_info.get("gpu", False):
                if "cu" in tag_name:
                    return release["tag_name"].replace("v", "")
            elif system_info.get("metal", False):
                if "metal" in tag_name:
                    return release["tag_name"].replace("v", "")
            else:
                if "cu" not in tag_name and "metal" not in tag_name:
                    return release["tag_name"].replace("v", "")
        return "0.2.20"
    except Exception:
        return "0.2.20"


def install_llama_package(package_name, custom_command=None):
    try:
        if not package_is_installed(package_name):
            print(f"Installing {package_name}...")
            command = [sys.executable, "-m", "pip", "install", package_name, "--no-cache-dir"]
            if custom_command:
                command += custom_command.split()
            subprocess.check_call(command)
        else:
            print(f"{package_name} is already installed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")


def package_is_installed(package_name):
    try:
        importlib.metadata.version(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False

def install_llama(system_info):
    try:
        imported = package_is_installed("llama-cpp-python") or package_is_installed("llama_cpp")

        if imported:
            print("llama-cpp-python installed")
        elif "fast_installed" in api_keys and api_keys["fast_installed"] == "True":
            print("The installation of llama-cpp-python was skipped")
            print(f"如果你想要安装llama-cpp-python，请在{config_path}中的[API_KEYS]添加或者修改fast_installed= False,然后然后重新运行程序。\nIf you want to install llama-cpp-python, please add or modify fast_installed= False in {config_path} in [API_KEYS] and then run the program again.")
        else:
            if system_info.get("gpu", False):
                cuda_version = system_info["cuda_version"]
                custom_command = f"--index-url  https://abetlen.github.io/llama-cpp-python/whl/{cuda_version}/"
                print(f"{cuda_version}: pip install llama-cpp-python --no-cache-dir {custom_command}"+"\n如果下载速度太慢，请直接到这个链接里下载轮子，然后手动安装。\nIf the download speed is too slow, please go directly to this link to download the wheel and install it manually.")
            elif system_info.get("metal", False):
                custom_command = f"--index-url  https://abetlen.github.io/llama-cpp-python/whl/metal/"
                print("mps:" +f" pip install llama-cpp-python --no-cache-dir {custom_command}"+"\n如果下载速度太慢，请直接到这个链接里下载轮子，然后手动安装。\nIf the download speed is too slow, please go directly to this link to download the wheel and install it manually.")
            else:
                custom_command = f"--index-url  https://abetlen.github.io/llama-cpp-python/whl/cpu/"
                print("cpu:" +f" pip install llama-cpp-python --no-cache-dir {custom_command}"+"\n如果下载速度太慢，请直接到这个链接里下载轮子，然后手动安装。\nIf the download speed is too slow, please go directly to this link to download the wheel and install it manually.")
            print("如果你选择手动下载llama-cpp-python，请确保下载的版本与你的系统匹配。然后使用以下命令手动安装：\nIf you choose to download llama-cpp-python manually, please make sure that the version you download matches your system. Then use the following command to manually install:")
            print("pip install <path_to_wheel_file> --no-cache-dir")
            print("请将 <path_to_wheel_file> 替换为你下载的轮子文件的路径。\nPlease replace <path_to_wheel_file> with the path to the wheel file you downloaded.")
            print(f"如果你想要跳过llama-cpp-python的安装，请在{config_path}中的[API_KEYS]添加或者修改fast_installed= True，然后重新运行程序。\nIf you want to skip the installation of llama-cpp-python, please add or modify fast_installed= True in {config_path} in [API_KEYS], and then run the program again.")
            install_llama_package("llama-cpp-python", custom_command=custom_command)
    except Exception as e:
        print(f"Error installing llama-cpp-python: {e}")



def get_system_info():
    system_info = {
        "gpu": False,
        "cuda_version": None,
        "avx2": False,
        "python_version": get_python_version(),
        "os": platform.system(),
        "os_bit": platform.architecture()[0].replace("bit", ""),
        "platform_tag": None,
        "metal": False  # 添加metal参数
    }

    # 检查NVIDIA GPU和CUDA版本
    if importlib.util.find_spec("torch"):
        import torch
        system_info["gpu"] = torch.cuda.is_available()
        if system_info["gpu"]:
            system_info["cuda_version"] = "cu" + torch.version.cuda.replace(".", "").strip()
            # 如果cuda_version高于cu124,则使用cu124
            # 提取cuda_version中的数字部分
            cuda_version_number = int("".join(filter(str.isdigit, system_info["cuda_version"])))
            if cuda_version_number > 124:
                system_info["cuda_version"] = "cu124"
    # 检查AVX2支持
    if importlib.util.find_spec("cpuinfo"):
        try:
            import cpuinfo
            cpu_info = cpuinfo.get_cpu_info()
            if cpu_info and "flags" in cpu_info:
                system_info["avx2"] = "avx2" in cpu_info["flags"]
            else:
                system_info["avx2"] = False
        except Exception as e:
            print(f"Error retrieving CPU information: {e}")
            system_info["avx2"] = False
    else:
        print("cpuinfo module not available.")
        system_info["avx2"] = False

    # 使用PyTorch检查macOS上的Metal支持
    if system_info["os"] == "Darwin":
        if torch.backends.mps.is_available():
            system_info["metal"] = True
        else:
            system_info["metal"] = False

    # 确定平台标签
    if importlib.util.find_spec("packaging.tags"):
        system_info["platform_tag"] = next(packaging.tags.sys_tags()).platform

    return system_info


def check_and_uninstall_websocket():
    # 获取当前Python解释器的路径
    interpreter = sys.executable

    # 检查websocket库是否已安装
    installed_packages = {dist.metadata['Name'].lower() for dist in importlib.metadata.distributions()}
    websocket_installed = "websocket" in installed_packages
    websocket_client_installed = "websocket-client" in installed_packages

    # 如果websocket库已安装，卸载websocket和websocket-client库
    if websocket_installed:
        packages_to_uninstall = []
        packages_to_uninstall.append("websocket")
        packages_to_uninstall.append("websocket-client")

        try:
            subprocess.check_call([interpreter, "-m", "pip", "uninstall", "-y"] + packages_to_uninstall)
            print("已成功卸载: " + ", ".join(packages_to_uninstall))
        except subprocess.CalledProcessError as e:
            print("卸载过程中出现错误：", e)
        # 重新安装websocket-client库
        try:
            subprocess.check_call([interpreter, "-m", "pip", "install", "websocket-client"])
            print("websocket-client库已成功重新安装。")
        except subprocess.CalledProcessError as e:
            print("重新安装过程中出现错误：", e)


def init_temp():
    # 构建prompt.json的绝对路径，如果temp文件夹不存在就创建
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(current_dir_path, "temp"), exist_ok=True)

def install_homebrew():
    try:
        result = subprocess.run(["brew", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Homebrew is not installed. Please install Homebrew first.")
            print("You can install Homebrew by running the following command:")
            print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            return False
        else:
            print("Homebrew is already installed.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error checking Homebrew installation: {e}")
        return False

def install_portaudio():
    try:
        if os.name == "posix":
            if sys.platform == "linux" or sys.platform == "linux2":
                result = subprocess.run(["cat", "/etc/os-release"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "EndeavourOS" in result.stdout or "Arch" in result.stdout:
                    result = subprocess.run(["pacman", "-Q", "portaudio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        os.system("pacman -Sy")
                        os.system("pacman -S --noconfirm portaudio")
                    else:
                        print("portaudio is already installed.")
                elif "CentOS" in result.stdout or "Red Hat" in result.stdout:
                    result = subprocess.run(["rpm", "-q", "portaudio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        os.system("yum update")
                        os.system("yum install -y portaudio")
                    else:
                        print("portaudio is already installed.")
                elif "Fedora" in result.stdout:
                    result = subprocess.run(["rpm", "-q", "portaudio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        os.system("dnf update")
                        os.system("dnf install -y portaudio")
                    else:
                        print("portaudio is already installed.")
                elif "openSUSE" in result.stdout:
                    result = subprocess.run(["rpm", "-q", "portaudio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        os.system("zypper refresh")
                        os.system("zypper install -y portaudio")
                    else:
                        print("portaudio is already installed.")
                else:
                    result = subprocess.run(["dpkg", "-s", "libportaudio2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        os.system("apt-get update")
                        os.system("apt-get install -y libportaudio2 libasound-dev")
                    else:
                        print("libportaudio2 is already installed.")
            elif sys.platform == "darwin":
                if install_homebrew():
                    result = subprocess.run(["brew", "list", "portaudio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        os.system("brew update")
                        os.system("brew install portaudio")
                    else:
                        print("portaudio is already installed.")
        elif os.name == "nt":
            pass
        else:
            print("Unsupported operating system")
    except subprocess.CalledProcessError as e:
        print(f"Error installing PortAudio library: {e}")


def uninstall_package(package_name):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", package_name], capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Failed to uninstall {package_name}: {result.stderr}")
    else:
        print(f"Successfully uninstalled {package_name}")


def install_package(package_name):
    result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to install {package_name}: {result.stderr}")
    else:
        print(f"Successfully installed {package_name}")


def manage_discord_packages():
    # 检查并卸载 discord.py 和 discord.py[voice]
    if package_is_installed("discord.py"):
        uninstall_package("discord.py")

    if package_is_installed("discord.py[voice]"):
        uninstall_package("discord.py[voice]")

    # 检查并安装 py-cord[voice]
    if not package_is_installed("py-cord[voice]"):
        install_package("py-cord[voice]")
    else:
        print("py-cord[voice] is already installed")



