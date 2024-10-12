import re


class Lorebook:
    def __init__(self):
        self._book_txt = ""
        self._book_dict = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"multiline": True, "default": "什么是lorebook？"}),
                "book_txt": ("STRING", {"multiline": True, "default": "lorebook:Lorebook（也称为世界信息或Memory Books）是一种工具，用于增强AI对世界细节的理解。\nLLM party:ComfyUI LLM Party 是一个基于 ComfyUI 的工具集，旨在帮助用户快速构建和集成大语言模型（LLM）工作流。"}),
            },
        }

    RETURN_TYPES = (
        "STRING",
    )
    RETURN_NAMES = (
        "user_prompt",
    )

    FUNCTION = "book"

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def _generate_book_dict(self):
        lines = self._book_txt.strip().split('\n')
        self._book_dict = {}
        for line in lines:
            # Use regex to split by the first occurrence of either Chinese or English colon
            parts = re.split(r'[:：]', line, maxsplit=1)
            if len(parts) == 2:
                key, value = parts
                self._book_dict[key.strip()] = value.strip()

        

    def set_book_txt(self, book_txt):
        self._book_txt = book_txt
        self._generate_book_dict()

    def book(self, user_prompt, book_txt):
        if book_txt != self._book_txt:
            self.set_book_txt(book_txt)
        print(self._book_dict)
        def get_values_from_keys(user_prompt):
            book=""
            # 对字典中的每一个key都判断一下是否存在于user_prompt中
            for key in self._book_dict.keys():
                if key in user_prompt:
                    # 字典中这个key以及其对应的value加入book
                    book += f"{key}: {self._book_dict[key]}\n"
            if book == "":
                return user_prompt
            else:
                return user_prompt+"\n"+"背景知识："+book
                    

        return (get_values_from_keys(user_prompt),)

if __name__ == "__main__":
    lorebook_instance = Lorebook()
    user_prompt = "Title和Year分别是什么时"
    book_txt = """
    Title: The Great Gatsby
    Author: F. Scott Fitzgerald
    Year: 1925
    Genre: Fiction
    """
    print(lorebook_instance.book(user_prompt, book_txt))
