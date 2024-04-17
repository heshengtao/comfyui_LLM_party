# -*- coding: utf-8 -*-

import os
import subprocess
import requests
from tqdm import tqdm  # Import the tqdm library for progress bar

def download_model_with_progress(model_url, local_path):
    # 初始化已下载的大小
    downloaded = 0
    try:
        # 获取文件的总大小
        with requests.get(model_url, stream=True) as r:
            total_size = int(r.headers.get('content-length', 0))

        # 如果本地文件已存在，获取已下载的文件大小
        if os.path.exists(local_path):
            downloaded = os.path.getsize(local_path)

        # 设置请求头，告诉服务器我们想从哪个字节开始下载
        headers = {'Range': f'bytes={downloaded}-'}

        # 请求服务器，从上次下载的地方继续下载
        with requests.get(model_url, headers=headers, stream=True, timeout=50) as r:
            r.raise_for_status()
            block_size = 8192  # Chunk size for updating the progress bar
            with open(local_path, "ab") as f:
                # 使用tqdm创建进度条
                progress = tqdm(initial=downloaded, total=total_size, unit='B', unit_scale=True, desc='Downloading')
                for data in r.iter_content(block_size):
                    f.write(data)
                    # 更新进度条
                    progress.update(len(data))
                # 关闭进度条
                progress.close()
        print(f"Model downloaded successfully to {local_path}")
    except requests.exceptions.RequestException as e:
        # 如果发生请求异常，打印错误信息
        print(f"Error downloading the model: {str(e)}")
# 检查模型是否已经下载
current_dir_path = os.path.dirname(os.path.realpath(__file__))
embeddings_dir = os.path.join(current_dir_path, "model")
embeddings_path = os.path.join(embeddings_dir, 'bge-large-zh')

# 如果模型文件夹不存在，则创建文件夹
if not os.path.exists(embeddings_dir):
    os.makedirs(embeddings_dir)

print(embeddings_path)
# 如果模型不存在，则克隆GitHub仓库
if not os.path.exists(embeddings_path):
    print("正在从github克隆模型...")
    model_git_url = "https://github.com/jsonzhuwei/bge-large-zh.git"
    try:
        subprocess.run(["git", "clone", model_git_url, embeddings_path], timeout=300)  # 设置超时时间为300秒
    except subprocess.TimeoutExpired:
        print("git clone 命令执行超时。")

else:
    print("模型已存在。")

custom_path = os.path.join(embeddings_dir, "bge-large-zh", "pytorch_model.bin")
if not os.path.exists(custom_path):
    model_url = "https://www.modelscope.cn/api/v1/models/AI-ModelScope/bge-large-zh/repo?Revision=master&FilePath=pytorch_model.bin"
    try:
        download_model_with_progress(model_url, custom_path)
    except Exception as e:
        print(f"Error downloading the model: {str(e)}")
if not os.path.exists(custom_path):
    model_url = "https://huggingface.co/BAAI/bge-large-zh-v1.5/resolve/main/pytorch_model.bin?download=true"
    try:
        download_model_with_progress(model_url, custom_path)
    except Exception as e:
        print(f"Error downloading the model: {str(e)}")
