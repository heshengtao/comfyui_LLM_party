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

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def notify(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif (
                not isinstance(extra_pnginfo[0], dict)
                or "workflow" not in extra_pnginfo[0]
            ):
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
· 从最基础的 LLM 多工具调用、角色设定快速搭建自己的专属AI助手、到可以行业落地的词向量RAG、GraphRAG来本地化的管理行业内知识库；
· 从单一的智能体流水线，到复杂的智能体与智能体辐射状交互模式、环形交互模式的构建；
· 从个人用户需要的接入自己的社交APP（QQ、飞书、Discord），到流媒体工作者需要的一站式LLM+TTS+ComfyUI工作流；
· 从普通学生所需要的第一个LLM应用的简单上手起步，到科研工作者们常用的各类参数调试接口，模型适配。
ComfyUI LLM Party is dedicated to creating a powerful LLM Agent ecosystem in the open source ecosystem of ComfyUI, bridging the gap between LLM and image generation, and making ComfyUI a mobile interface that can be connected to everything. Zero code realizes the creation of personal AI Agents, with low barriers and strong degrees of freedom.
· From the most basic LLM multi-tool call, role setting to quickly build your own exclusive AI assistant, to word vector RAG and GraphRAG that can be localized to manage the knowledge base in the industry;
· From a single agent pipeline to the construction of complex agent-agent radial interaction mode and circular interaction mode;
· From individual users' access to their own social apps (QQ, Feishu, Discord), to one-stop LLM + TTS + ComfyUI workflows for streaming media workers.
· From the simple beginnings of the first LLM application required by ordinary students, to the various parameter debugging interfaces commonly used by researchers, model adaptation.
注意！本项目是基于AGPL协议开源的，请遵守AGPL协议，以避免不必要的法律问题！谢谢您的合作！如果您需要可以闭源商用的版本，请邮箱联系hst97@qq.com
Attention! This project is open source based on the AGPL agreement, please abide by the AGPL agreement to avoid unnecessary legal problems! Thank you for your cooperation! If you need a closed-source commercial version, please contact hst97@qq.com
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
