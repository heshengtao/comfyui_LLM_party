from langchain_text_splitters import RecursiveCharacterTextSplitter


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
                "file_content": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
            },
            "optional": {"chunk_size": ("INT", {"default": 1024}), "chunk_overlap": ("INT", {"default": 0})},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, file_content, chunk_size=1024, chunk_overlap=0, is_enable=True, is_reload=False):
        if not is_enable:
            return (None,)
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
        # 分段输出
        if self.index < len(self.text_splitter.split_text(self.file_content)):
            out = self.text_splitter.split_text(self.file_content)[self.index]
            print("当前索引：", self.index)
            print("当前输出：", out)
            self.index += 1
            return (out,)
        else:
            return (None,)

    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record
