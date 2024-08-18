import importlib
import inspect
import os
import platform
import re
import shutil
import subprocess
import sys

import packaging.tags
import pkg_resources
import torch
from requests import get


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
    if not package_is_installed(package_name):
        print(f"Installing {package_name}...")
        command = [sys.executable, "-m", "pip", "install", package_name, "--no-cache-dir"]
        if custom_command:
            command += custom_command.split()
        subprocess.check_call(command)
    else:
        print(f"{package_name} is already installed.")


def package_is_installed(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False
def extract_version(tag_name):
    pattern = r'(\d+\.\d+\.\d+)-'
    match = re.search(pattern, tag_name)
    if match:
        return match.group(1)
    else:
        print(f"No match found for: {tag_name}")
    return None

def install_llama(system_info):
    imported = package_is_installed("llama-cpp-python") or package_is_installed("llama_cpp")
    if imported:
        print("llama-cpp installed")
    else:
        lcpp_version = latest_lamacpp(system_info)
        base_url = "https://github.com/abetlen/llama-cpp-python/releases/download/v"
        avx = "AVX2" if system_info["avx2"] else "AVX"
        python_version = get_python_version()
        if system_info.get("gpu", False):
            cuda_version = system_info["cuda_version"]
            custom_command = f"--force-reinstall --no-deps --index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/{avx}/{cuda_version}"
            print("cuda"+custom_command)
        elif system_info.get("metal", False):
            tag=extract_version(lcpp_version)
            custom_command = f"{base_url}{lcpp_version}/llama_cpp_python-{tag}-cp{python_version}-cp{python_version}-{system_info['platform_tag']}.whl"
            print("mps"+custom_command)
        else:
            custom_command = f"{base_url}{lcpp_version}/llama_cpp_python-{lcpp_version}-cp{python_version}-cp{python_version}-{system_info['platform_tag']}.whl"
            print("cpu"+custom_command)
        install_llama_package("llama-cpp-python", custom_command=custom_command)


def get_comfy_dir():
    # 获取当前脚本文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前脚本文件所在目录
    current_dir = os.path.dirname(current_file_path)
    # 获取目标目录的绝对路径
    comfy_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    # 获取"web/extensions/party"目录的绝对路径
    comfy_dir = os.path.join(comfy_dir, "web/extensions/party")
    return comfy_dir


def copy_js_files():
    # 设置当前文件夹路径和目标文件夹路径
    current_folder = os.path.dirname(os.path.abspath(__file__))
    target_folder = get_comfy_dir()

    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 清空目标文件夹里所有文件
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

        except Exception as e:
            print(f"无法删除文件 {file_path}: {e}")

    # 获取当前文件夹中web子文件夹下的所有.js文件
    js_files = [f for f in os.listdir(os.path.join(current_folder, "web")) if f.endswith(".js")]

    # 复制文件
    for file_name in js_files:
        source_file = os.path.join(current_folder, "web", file_name)
        target_file = os.path.join(target_folder, file_name)
        shutil.copy2(source_file, target_file)


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
    if "macosx" in system_info['platform_tag'] and system_info["metal"] == True:
        system_info["platform_tag"] = "macosx_11_0_arm64"
    elif "macosx" in system_info['platform_tag'] and system_info["metal"] == False:
        system_info["platform_tag"] = "macosx_10_9_x86_64"

    return system_info


def check_and_uninstall_websocket():
    # 获取当前Python解释器的路径
    interpreter = sys.executable

    # 检查websocket库是否已安装
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
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
import shlex
def install_homebrew():
    try:
        # 检查是否能访问 GitHub
        github_url = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
        gitee_url = "https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh"
        
        # 尝试访问 GitHub
        if subprocess.call(["curl", "-fsSL", github_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            command = f'/bin/bash -c "$(curl -fsSL {github_url})"'
        else:
            print("无法访问 GitHub，尝试使用国内镜像源...")
            command = f'/bin/bash -c "$(curl -fsSL {gitee_url})"'
        
        subprocess.check_call(shlex.split(command))
        print("Homebrew 已成功安装。")
    except subprocess.CalledProcessError as e:
        print(f"安装 Homebrew 失败: {e}")
        return False
    except Exception as e:
        print(f"发生了意外错误: {e}")
        return False
    return True

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
                pass
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


install_portaudio()
check_and_uninstall_websocket()

# 调用函数
copy_js_files()
system_info = get_system_info()
install_llama(system_info)
init_temp()
# 调用函数
manage_discord_packages()
