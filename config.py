# 获取当前文件的绝对路径
import configparser
import os
from langchain.embeddings import HuggingFaceBgeEmbeddings
import subprocess

# 检查模型是否已经下载
current_dir_path = os.path.dirname(os.path.realpath(__file__))
embeddings_dir = os.path.join(current_dir_path, "model")
embeddings_path = os.path.join(embeddings_dir, 'bge-large-zh')


current_file_path = os.path.abspath(__file__)

# 获取当前文件所在目录的路径
current_dir_path = os.path.dirname(current_file_path)

# 构建config.ini的绝对路径
config_path = os.path.join(current_dir_path, 'config.ini')



def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    
    api_keys = {}
    if 'API_KEYS' in config:
        api_keys = config['API_KEYS']
    
    return api_keys

# 加载词嵌入模型

model_kwargs = {'device': 'cuda'}  # 如果您有GPU，可以设置为 'cuda'，否则使用 'cpu'
encode_kwargs = {'normalize_embeddings': True}  # 设置为 True 以计算余弦相似度

bge_embeddings = HuggingFaceBgeEmbeddings(
    model_name=embeddings_path,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
if __name__ == "__main__":
    pass