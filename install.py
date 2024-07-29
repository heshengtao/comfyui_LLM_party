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
from server import PromptServer


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
            if system_info['gpu']:
                if "cuda" in tag_name:
                    return release["tag_name"].replace("v", "")
            elif system_info['metal']:
                if "metal" in tag_name:
                    return release["tag_name"].replace("v", "")
            else:
                if "cuda" not in tag_name and "metal" not in tag_name:
                    return release["tag_name"].replace("v", "")
        return "0.2.20"
    except Exception:
        return "0.2.20"

def install_package(package_name, custom_command=None):
    if not package_is_installed(package_name):
        print(f"Installing {package_name}...")
        command = [sys.executable, "-m", "pip", "install", package_name, "--no-cache-dir"]
        if custom_command:
            command += custom_command.split()
        subprocess.check_call(command)
    else:
        print(f"{package_name} is already installed.")

def package_is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_llama(system_info):
    imported = package_is_installed("llama-cpp-python") or package_is_installed("llama_cpp")
    if imported:
        print("llama-cpp installed")
    else:
        lcpp_version = latest_lamacpp(system_info)
        base_url = "https://github.com/abetlen/llama-cpp-python/releases/download/v"
        avx = "AVX2" if system_info['avx2'] else "AVX"
        python_version = get_python_version()
        if system_info['gpu']:
            cuda_version = system_info['cuda_version']
            custom_command = f"--force-reinstall --no-deps --index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/{avx}/{cuda_version}"
        elif system_info['metal']:
            custom_command = f"{base_url}{lcpp_version}/llama_cpp_python-{lcpp_version}-cp{python_version}-cp{python_version}-macosx_11_0_arm64.whl"
        else:
            custom_command = f"{base_url}{lcpp_version}/llama_cpp_python-{lcpp_version}-cp{python_version}-cp{python_version}-{system_info['platform_tag']}.whl"
        install_package("llama-cpp-python", custom_command=custom_command)


def get_comfy_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(inspect.getfile(PromptServer))
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def copy_js_files():
    # 设置当前文件夹路径和目标文件夹路径
    current_folder = os.path.dirname(os.path.abspath(__file__))
    target_folder = get_comfy_dir("web/extensions/party")

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
    """Gather system information related to NVIDIA GPU, CUDA version, AVX2 support, Python version, OS, and platform tag."""
    system_info = {
        "gpu": False,
        "cuda_version": None,
        "avx2": False,
        "python_version": get_python_version(),
        "os": platform.system(),
        "os_bit": platform.architecture()[0].replace("bit", ""),
        "platform_tag": None,
    }

    # Check for NVIDIA GPU and CUDA version
    if importlib.util.find_spec("torch"):
        system_info["gpu"] = torch.cuda.is_available()
        if system_info["gpu"]:
            system_info["cuda_version"] = "cu" + torch.version.cuda.replace(".", "").strip()

    # Check for AVX2 support
    if importlib.util.find_spec("cpuinfo"):
        try:
            # Attempt to import the cpuinfo module
            import cpuinfo

            # Safely attempt to retrieve CPU flags
            cpu_info = cpuinfo.get_cpu_info()
            if cpu_info and "flags" in cpu_info:
                # Check if 'avx2' is among the CPU flags
                system_info["avx2"] = "avx2" in cpu_info["flags"]
            else:
                # Handle the case where CPU info is unavailable or does not contain 'flags'
                system_info["avx2"] = False
        except Exception as e:
            # Handle unexpected errors gracefully
            print(f"Error retrieving CPU information: {e}")
            system_info["avx2"] = False
    else:
        # Handle the case where the cpuinfo module is not installed
        print("cpuinfo module not available.")
        system_info["avx2"] = False
    # Determine the platform tag
    if importlib.util.find_spec("packaging.tags"):
        system_info["platform_tag"] = next(packaging.tags.sys_tags()).platform

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


def install_portaudio():
    try:
        if os.name == "posix":
            if sys.platform == "linux" or sys.platform == "linux2":
                # Linux
                result = subprocess.run(["dpkg", "-s", "libportaudio2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    os.system("apt-get update")
                    os.system("apt-get install -y libportaudio2 libasound-dev")
                else:
                    print("libportaudio2 已经安装")
            elif sys.platform == "darwin":
                # macOS
                result = subprocess.run(["brew", "list", "portaudio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    subprocess.check_call(["brew", "install", "portaudio"])
                else:
                    print("portaudio 已经安装")
        elif os.name == "nt":
            pass
        else:
            print("不支持的操作系统")
    except subprocess.CalledProcessError as e:
        print(f"安装 PortAudio 库时出错: {e}")


install_portaudio()
check_and_uninstall_websocket()

# 调用函数
copy_js_files()
system_info = get_system_info()
install_llama(system_info)
init_temp()
