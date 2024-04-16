
import os
import subprocess

# 检查模型是否已经下载
current_dir_path = os.path.dirname(os.path.realpath(__file__))
embeddings_dir = os.path.join(current_dir_path, "model")
embeddings_path = os.path.join(embeddings_dir, 'bge-large-zh')

# 如果模型文件夹不存在，则创建文件夹
if not os.path.exists(embeddings_dir):
    os.makedirs(embeddings_dir)

# 如果模型不存在，则克隆GitHub仓库
if not os.listdir(embeddings_path):
    try:
        print("正在从GitHub克隆模型...")
        model_git_url = "https://github.com/jsonzhuwei/bge-large-zh.git"  # 模型的GitHub仓库链接
        subprocess.run(["git", "clone", model_git_url, embeddings_path])
        print("模型克隆完成。")
    except:
        print("正在从modelscope克隆模型...")
        model_git_url = "https://www.modelscope.cn/AI-ModelScope/bge-large-zh.git"
        subprocess.run(["git", "clone", model_git_url, embeddings_path])
        print("模型克隆完成。")
else:
    print("模型已存在。")