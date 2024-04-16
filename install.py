
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
                for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit="B", unit_scale=True):
                    f.write(data)
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
    try:
        print("正在从modelscope克隆模型...")
        model_git_url = "https://www.modelscope.cn/AI-ModelScope/bge-large-zh.git"
        subprocess.run(["git", "clone", model_git_url, embeddings_path])


        print("模型克隆完成。")
    except subprocess.CalledProcessError as e:
        print(f"模型克隆失败：{e}")
else:
    print("模型已存在。")
    
model_url = "https://www.modelscope.cn/api/v1/models/AI-ModelScope/bge-large-zh/repo?Revision=master&FilePath=pytorch_model.bin"
custom_path = os.path.join(embeddings_dir, "bge-large-zh", "pytorch_model.bin")
download_model_with_progress(model_url, custom_path)