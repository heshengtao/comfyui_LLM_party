<p align="right">
   <a href="./README_ZH.md">中文</a> |  <strong>English</strong>
</p>

## Latest update
1. The [chatTTS](https://github.com/2noise/ChatTTS) node has been added, thank you very much for the contribution of [guobalove](https://github.com/guobalove)! `model_path` parameter can be empty! It is recommended to use `HF` mode to load the model, the model will be automatically downloaded from hugging face, no need to download manually; if using `local` loading, please put the model's`asset` and `config` folders in the root directory. [Baidu cloud address](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), extraction code: qyhu; if using `custom` mode to load, please put the model's `asset` and `config` folders under `model_path`.

# **COMFYUI LLM PARTY—A Node Library for LLM Workflow Development in ComfyUI**

## Introduction
[comfyui](https://github.com/comfyanonymous/ComfyUI) is an extremely minimalist UI interface, primarily used for AI drawing and other workflows based on the SD model. C‌‌﻿​﻿‎﻿​﻿‎‏​﻿‍‎​﻿‎﻿​﻿‎‏​﻿‌‎​﻿‎‍​﻿‍‏​‍﻿‌​﻿‌‏omfyui_llm_party aims to develop a complete set of nodes for LLM workflow construction based on comfyui. It allows users to quickly and conveniently build their own LLM workflows and easily integrate them into their existing SD workflows.The picture shows a workflow of LLM implementing multi-tool calling, for more workflows please refer to the [workflow](workflow) folder.

![图片](img/多工具调用.png)

## User Guide
1. [Building a Modular AI with ComfyUI×LLM: A Step-by-Step Tutorial (Super Easy!)](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [Teach you GPT-4o access to comfyui | Make workflow call another workflow | Make LLM a tool](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [Disguise your workflow as GPT to access WeChat | Omost compatible! Flexibly create your own dalle3](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [How to play interactive fiction games in comfyui](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. For the instructions for using the node, please refer to: [how to use nodes](how_to_use_nodes.md)

6. If there are any issues with the plugin or you have other questions, feel free to join the QQ group: [931057213](img/Q群.jpg).

## Model support
1. Support all API calls in openai format, base_url selection reference [config.ini.example](config.ini.example), which has been tested so far:
* [ollama](https://github.com/ollama/ollama)
* [Tongyi Qianwen /qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [zhipu qingyan/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)

2. Most of the local models supported by the transformer library have been tested so far:
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b)
* [meta-llama/llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)

3. Model download
* [Baidu cloud address](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), extraction code: qyhu
## Features
1. You can right-click in the comfyui interface, select `llm` from the context menu, and you will find the nodes for this project. [how to use nodes](how_to_use_nodes.md)
2. Supports API integration or local large model integration. Modular implementation for tool invocation.When entering the base_url, please use a URL that ends with `/v1/`.You can use [ollama](https://github.com/ollama/ollama) to manage your model. Then, enter `http://127.0.0.1:11434/v1/` for the base_url, `ollama` for the api_key, and your model name for the model_name, such as: llama3.
- API access sample workflow: [start_with_LLM_api](workflow/start_with_LLM_api)
- Local model access sample workflow: [start_with_LLM_local](workflow/start_with_LLM_local)
- ollama access sample workflow: [ollama](workflow/ollama.json)
3. Local knowledge base integration with RAG support.sample workflow: [Knowledge Base RAG Search](workflow/知识库RAG搜索.json)
4. Ability to invoke code interpreters.
5. Enables online queries, including Google search support.sample workflow: [movie query workflow](workflow/电影查询工作流.json)
6. Implement conditional statements within ComfyUI to categorize user queries and provide targeted responses.sample workflow: [intelligent customer service](workflow/智能客服.json)
7. Supports looping links for large models, allowing two large models to engage in debates.sample workflow: [Tram Challenge Debate](workflow/电车难题辩论赛.json)
8. Attach any persona mask, customize prompt templates.
9. Supports various tool invocations, including weather lookup, time lookup, knowledge base, code execution, web search, and single-page search.
10. Use LLM as a tool node.sample workflow: [LLM Matryoshka dolls](workflow/LLM套娃.json)
11. Rapidly develop your own web applications using API + Streamlit.The picture below is an example of a drawing application.
12. Added a dangerous omnipotent interpreter node that allows the large model to perform any task.
13. It is recommended to use the `show_text` node under the `function` submenu of the right-click menu as the display output for the LLM node.
14. Supported the visual features of GPT-4O!sample workflow:[GPT-4o](workflow/GPT-4o.json)
15. A new workflow intermediary has been added, which allows your workflow to call other workflows!sample workflow:[Invoke another workflow](workflow/调用另一个工作流.json)
16. Adapted to all models with an interface similar to OpenAI, such as: Tongyi Qianwen/QWEN, Zhigu Qingyan/GLM, DeepSeek, Kimi/Moonshot. Please fill in the base_url, api_key, and model_name of these models into the LLM node to call them.
17. Added an LVM loader, now you can call the LVM model locally, support [lava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf) model, other LVM models should theoretically run if they are GUFF format.The example workflow can be found here: [start_with_LVM.json](workflow/start_with_LVM.json).
18. I wrote a `fastapi.py` file, and if you run it directly, you’ll get an OpenAI interface on `http://127.0.0.1:8817/v1/`. Any application that can call GPT can now invoke your comfyui workflow! I will create a tutorial to demonstrate the details on how to do this.
19. I’ve separated the LLM loader and the LLM chain, dividing the model loading and model configuration. This allows for sharing models across different LLM nodes!
20. macOS and mps devices are now supported! Thanks to [bigcat88](https://github.com/bigcat88) for their contribution!
21. You can build your own interactive novel game, and go to different endings according to the user's choice! Example workflow reference: [interactive_novel](workflow/互动小说.json)
22. Adapted to OpenAI's whisper and tts functions, voice input and output can be realized. Example workflow reference: [voice_input&voice_output](workflow/语音输入+语音输出.json)
23. Compatible with [Omost](https://github.com/lllyasviel/Omost)!!! Please download [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) to experience it now! Sample workflow reference: [start_with_OMOST](workflow/start_with_OMOST)
24. Added LLM tools to send messages to WeCom, DingTalk, and Feishu, as well as external functions to call.
25. Added a new text iterator, which can output only part of the characters at a time. It is safe to split the text according to Carriage Return and chunk size, and will not be divided from the middle of the text. chunk_overlap refers to how many characters the divided text overlaps. In this way, you can enter super long text in batches, as long as you don't have a brain to click, or open the loop in comfyui to execute, it can be automatically executed. Remember to turn on the is_locked property, which can automatically lock the workflow at the end of the input and will not continue to execute. Example workflow: [text iteration input](workflow/文本迭代输入.json)
26. Added the model name attribute to the local LLM loader, local llava loader, and local guff loader. If it is empty, it will be loaded using various local paths in the node. If it is not empty, it will be loaded using the path parameters you fill in yourself in `config.ini`. If it is not empty and not in `config.ini`, it will be downloaded from huggingface or loaded from the model save directory of huggingface. If you want to download from huggingface, please fill in the format of for example: `THUDM/glm-4-9b-chat`.Attention! Models loaded in this way must be adapted to the transformer library.
27. Adapted to [CosyVoice](https://github.com/FunAudioLLM/CosyVoice), now you can use the TTS function directly without downloading any model or any API key. Currently the interface is only adapted to Chinese.
28. Added JSON file parsing node and JSON value node, which allows you to get the value of a key from a file or text. Thanks to [guobalove](https://github.com/guobalove) for your contribution!
29. Improved the code of tool call. Now LLM without tool call function can also open is_tools_in_sys_prompt attribute (local LLM does not need to be opened by default, automatic adaptation). After opening, the tool information will be added to the system prompt word, so that LLM can call the tool.Related papers on implementation principles: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
30. A new custom_tool folder is created to store the code of the custom tool. You can refer to the code in the [custom_tool](custom_tool) folder, put the code of the custom tool into the custom_tool folder, and you can call the custom tool in LLM.
31. Added Knowledge Graph tool, so that LLM and Knowledge Graph can interact perfectly. LLM can modify Knowledge Graph according to your input, and can reason on Knowledge Graph to get the answers you need. Example workflow reference: [graphRAG_neo4j](workflow/graphRAG_neo4j.json)
32. Added personality AI function, 0 code to develop your own girlfriend AI or boyfriend AI, unlimited dialogue, permanent memory, stable personality. Example workflow reference: [Mylover Personality AI](workflow/麦洛薇人格AI.json)

![图片](img/画画应用.png)

## Download
Install using one of the following methods:
### Method 1:
1. Search for comfyui_LLM_party in the [comfyui manager](https://github.com/ltdrdata/ComfyUI-Manager) and install it with one click.
2. Restart comfyui.

### Method 2:
1. Navigate to the `custom_nodes` subfolder under the ComfyUI root folder.
2. Clone this repository with `git clone https://github.com/heshengtao/comfyui_LLM_party.git`.

### Method 3:
1. Click `CODE` in the upper right corner.
2. Click `download zip`.
3. Unzip the downloaded package into the `custom_nodes` subfolder under the ComfyUI root folder.

## Environment Deployment
1. Navigate to the `comfyui_LLM_party` project folder.
2. Enter `pip install -r requirements.txt` in the terminal to deploy the third-party libraries required by the project into the comfyui environment. Please ensure you are installing within the comfyui environment and pay attention to any `pip` errors in the terminal.
3. If you are using the comfyui launcher, you need to enter `path_in_launcher_configuration\python_embeded\python.exe -m pip install -r requirements.txt` in the terminal to install. The `python_embeded` folder is usually at the same level as your `ComfyUI` folder.
4. If you have some environment configuration problems, you can try to use the dependencies in `requirements_fixed.txt`.

## Configuration
Configure the APIKEY using one of the following methods:
### Method One:
1. Open the `config.ini` file in the `comfyui_LLM_party` project folder.
2. Enter your `openai_api_key` and `base_url` in `config.ini`.
3. If you want to use the Google search tool, enter your `google_api_key` and `cse_id` in `config.ini`.

### Method Two:
1. Open the comfyui interface.
2. Create a new Large Language Model (LLM) node and directly enter your `openai_api_key` and `base_url` in the node.
3. Create a new Google Search Tool (google_tool) node and directly enter your `google_api_key` and `cse_id` in the node.

## Next Steps Plan:
1. More model adaptations, at least covering the API interfaces of mainstream large models and local calls of mainstream open-source models, as well as more LVM model adaptations. Currently, I have only adapted the visual function calls of GPT-4;
2. More ways to build agents. The work I have completed in this area includes importing an LLM as a tool to another LLM, achieving radial construction of LLM workflows, and importing one workflow as a node into another workflow. I might develop some cooler functions in this area in the future.
3. More automation features. In the future, I will introduce more nodes that automatically push images, text, videos, and audio to other applications, as well as listening nodes that implement automatic replies to mainstream social software and forums.
4. More knowledge base management functions. The project already supports local file search and web search. In the future, I will introduce knowledge graph search and long-term memory search. This will allow agents to think logically about professional knowledge and always remember certain key information when conversing with users.
5. More tools, more persona. This part is the easiest to do but also requires the most accumulation. I hope that in the future, this project can have as many custom nodes as comfyui, with a multitude of tools and persona.

## Disclaimer:
This open-source project and its contents (hereinafter referred to as "Project") are provided for reference purposes only and do not imply any form of warranty, either expressed or implied. The contributors of the Project shall not be held responsible for the completeness, accuracy, reliability, or suitability of the Project. Any reliance you place on the Project is strictly at your own risk. In no event shall the contributors of the Project be liable for any indirect, special, or consequential damages or any damages whatsoever resulting from the use of the Project.

## Special thanks:
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Support:

### If my work has brought value to your day, consider fueling it with a coffee! Your support not only energizes the project but also warms the heart of the creator. ☕💖 Every cup makes a difference!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

### If there is a problem with the plug-in or you have other questions, welcome to join the QQ group: 931057213

<div style="display:flex; justify-content:space-between;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

### If you want to continue to pay attention to the latest features of this project, please follow the Bilibili account: [Bilibili artificial intelligence robot](https://space.bilibili.com/26978344)
