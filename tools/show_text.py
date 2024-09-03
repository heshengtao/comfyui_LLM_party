class show_text_party:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def notify(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]:
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [text]

        return {"ui": {"text": text}, "result": (text,)}


class About_us:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "大模型派对（llm_party）"

    def notify(self, unique_id=None, extra_pnginfo=None):
        text = [
            f"""
这是该项目的一个彩蛋节点。
comfyui_LLM_party
项目发起人：heshengtao
项目地址: https://github.com/heshengtao/comfyui_LLM_party
项目频道: https://space.bilibili.com/26978344?spm_id_from=333.1007.0.0
ComfyUI LLM Party是一个致力于在ComfyUI的开源生态中打造一个功能强大的LLM Agent生态，将LLM与图像生成领域之间的gap打通，同时将ComfyUI做成一个可万物互联的移动接口，零代码实现个人AI Agent的创造，门槛低，自由度强。
·从最基础的 LLM 多工具调用、角色设定快速搭建自己的专属AI助手、到可以行业落地的词向量RAG、GraphRAG来本地化的管理行业内知识库；
·从单一的智能体流水线，到复杂的智能体与智能体辐射状交互模式、环形交互模式的构建；
·从个人用户需要的接入自己的社交APP（QQ、飞书、Discord），到流媒体工作者需要的一站式LLM+TTS+ComfyUI工作流；
·从普通学生所需要的第一个LLM应用的简单上手起步，到科研工作者们常用的各类参数调试接口，模型适配。
        """.strip()
        ]
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]:
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    # 直接赋值，不进行转换
                    node["widgets_values"] = [text]
        return {"ui": {"text": text}, "result": (text,)}
