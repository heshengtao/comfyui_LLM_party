
import os
import subprocess
import requests
from tqdm import tqdm  # Import the tqdm library for progress bar

def download_model_with_progress(model_url, local_path):
    try:
        response = requests.get(model_url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192  # Chunk size for updating the progress bar
            with open(local_path, "wb") as f:
                # 使用tqdm创建进度条
                progress = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading')
                for data in response.iter_content(block_size):
                    f.write(data)
                    # 更新进度条
                    progress.update(len(data))
                # 关闭进度条
                progress.close()
            print(f"Model downloaded successfully to {local_path}")
        else:
            print(f"Failed to download the model. Status code: {response.status_code}")
    except Exception as e:
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