import os
import random
from langchain_text_splitters import RecursiveCharacterTextSplitter
import signal
import sys
import json
def interrupt_handler(signum, frame):
    print("Process interrupted")
    sys.exit(0)

class text_iterator:
    def __init__(self):
        self.index = 0
        self.record = 0
        self.file_content = ""
        self.chunk_size = 1024
        self.chunk_overlap = 0

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_content": ("STRING", {"forceInput": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
                "iterator_mode": (["sequential","random","Infinite", "sequential_flagout"], {"default": "sequential"}),
            },
            "optional": {"chunk_size": ("INT", {"default": 1024}), "chunk_overlap": ("INT", {"default": 0})},
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("file_content", "is_end")

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, file_content,iterator_mode, chunk_size=1024, chunk_overlap=0, is_enable=True, is_reload=False):
        flag_is_end = False
        if not is_enable:
            return (None, flag_is_end,)
        if (
            self.file_content != file_content
            or is_reload == True
            or self.chunk_size != chunk_size
            or self.chunk_overlap != chunk_overlap
        ):
            self.index = 0  # 重置索引为0，因为我们要从第二行开始读取数据
            self.file_content = file_content
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
        # 将file_content用RecursiveCharacterTextSplitter分割
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        text_len=len(self.text_splitter.split_text(self.file_content))
        # 分段输出
        if self.index >= text_len:
            self.index = 0
            if iterator_mode == "sequential":
                signal.signal(signal.SIGINT, interrupt_handler)
                signal.raise_signal(signal.SIGINT)  # 直接中断进程
        if self.index == text_len - 1 and iterator_mode == "sequential_flagout":
            flag_is_end = True
        out = self.text_splitter.split_text(self.file_content)[self.index]
        print("当前索引：", self.index)
        print("当前输出：", out)
        if iterator_mode == "sequential" or iterator_mode =="Infinite" or iterator_mode == "sequential_flagout":
            self.index += 1
        elif iterator_mode == "random":
            self.index = random.randint(0, text_len - 1)
        return (out, flag_is_end,)

    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record

class text_writing:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "file_path": ("STRING", {"default": ""}),
                "mode": (["a","w"], {"default": "a"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "suffix": ("STRING", {"default": "_processed"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)

    FUNCTION = "file"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, text, file_path,suffix,is_enable=True, mode="w"):
        if not is_enable:
            return (None,)
        try:
            # 获得root目录
            root_dir = os.path.dirname(file_path)
            # 如果目录不存在，则创建目录
            if not os.path.exists(root_dir):
                os.makedirs(root_dir)
            # 获取文件名和扩展名
            file_name, file_extension = os.path.splitext(file_path)
            # 添加后缀
            file_path = file_name + suffix + file_extension
            # 根据模式打开文件，并指定编码为UTF-8
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(text+"\n")
        except Exception as e:
            # 捕获并处理异常
            raise ValueError(f"写入文件失败: {e}")
        return (file_path,)
    
class json_writing:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "file_path": ("STRING", {"default": ""}),
                "mode": (["extend","append"], {"default": "extend"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)

    FUNCTION = "file"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, text, file_path,mode):
        try:
            # 确保file_path指向一个json文件
            if not file_path.endswith(".json"):
                raise ValueError("写入的文件必须是一个json文件")
            # 如果文件不存在，就创建一个空列表
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
            # 将json文件读取出来
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            #如果为空，就创建一个空列表
            if not data:
                data = []
            # 如果是extend模式，就将新的数据添加到列表中
            if mode == "extend":
                data.extend(json.loads(text))
            # 如果是append模式，就将新的数据添加到列表的末尾
            elif mode == "append":
                data.append(json.loads(text))
            # 将更新后的数据写回文件
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            # 捕获并处理异常
            raise ValueError(f"写入的文件必须是一个json文件，写入文件失败: {e}")
        return (file_path,)