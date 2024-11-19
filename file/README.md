![图片](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">text tutorial</a> ·
  <a href="workflow_tutorial/">workflow tutorial</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">Baidu cloud</a> ·
  <a href="img/Q群.jpg">QQ group</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">About us</a>  
</div>

####

<div align="center">
  <a href="./README_ZH.md"><img src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="./README_RU.md"><img src="https://img.shields.io/badge/Русский-d9d9d9"></a>
  <a href="./README_FR.md"><img src="https://img.shields.io/badge/Français-d9d9d9"></a> 
  <a href="./README_DE.md"><img src="https://img.shields.io/badge/Deutsch-d9d9d9"></a>
  <a href="./README_JA.md"><img src="https://img.shields.io/badge/日本語-d9d9d9"></a>
  <a href="./README_KO.md"><img src="https://img.shields.io/badge/한국어-d9d9d9"></a>
  <a href="./README_AR.md"><img src="https://img.shields.io/badge/العربية-d9d9d9"></a>
  <a href="./README_ES.md"><img src="https://img.shields.io/badge/Español-d9d9d9"></a>
  <a href="./README_PT.md"><img src="https://img.shields.io/badge/Português-d9d9d9"></a>
</div>

####

C‌‌﻿​﻿‎﻿​﻿‎‏​﻿‍‎​﻿‎﻿​﻿‎‏​﻿‌‎​﻿‎‍​﻿‍‏​‍﻿‌​﻿‌‏omfyui_llm_party aims to develop a complete set of nodes for LLM workflow construction based on [comfyui](https://github.com/comfyanonymous/ComfyUI) as the front end. It allows users to quickly and conveniently build their own LLM workflows and easily integrate them into their existing image workflows.

## Effect display
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## Project Overview

ComfyUI LLM Party, from the most basic LLM multi-tool call, role setting to quickly build your own exclusive AI assistant, to the industry-specific word vector RAG and GraphRAG to localize the management of the industry knowledge base; from a single agent pipeline, to the construction of complex agent-agent radial interaction mode and ring interaction mode; from the access to their own social APP (QQ, Feishu, Discord) required by individual users, to the one-stop LLM + TTS + ComfyUI workflow required by streaming media workers; from the simple start of the first LLM application required by ordinary students, to the various parameter debugging interfaces commonly used by scientific researchers, model adaptation. All of this, you can find the answer in ComfyUI LLM Party.

## Quick Start
1. Drag the following workflows into your comfyui, then use [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager) to install the missing nodes.
  - Use API to call LLM: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - Manage local LLM with ollama: [start_with_Ollama](workflow/ollama.json)
  - Use local LLM in distributed format: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - Use local LLM in GGUF format: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - Use local VLM in distributed format: [start_with_VLM_local](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json) (testing, currently only supports [Llama-3.2-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct))
  - Use local VLM in GGUF format: [start_with_VLM_GGUF](workflow/start_with_llava.json)
2. If you are using API, fill in your `base_url` (it can be a relay API, make sure it ends with `/v1/`), for example: `https://api.openai.com/v1/` and `api_key` in the API LLM loader node.
3. If you are using ollama, turn on the `is_ollama` option in the API LLM loader node, no need to fill in `base_url` and `api_key`.
4. If you are using a local model, fill in your model path in the local model loader node, for example: `E:\model\Llama-3.2-1B-Instruct`. You can also fill in the Huggingface model repo id in the local model loader node, for example: `lllyasviel/omost-llama-3-8b-4bits`.
5. Due to the high usage threshold of this project, even if you choose the quick start, I hope you can patiently read through the project homepage.

## Latest update
1. Forked [chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat), created a new repository [party-on-wechat](https://github.com/heshengtao/party-on-wechat). The installation and usage methods are the same as the original project, no configuration is required, just start the party's FastAPI. By default, it calls the wx_api workflow and supports image output. It will be updated gradually to ensure a smooth experience of party on WeChat.
2. Added an In-Context-LoRA mask node, used for generating consistent [In-Context-LoRA](https://github.com/ali-vilab/In-Context-LoRA/tree/main) prompts.
1. We have added a frontend component with features laid out from left to right as follows:
   - Saves your API key and Base URL to the `config.ini` file. When you use the `fix node` function on the API LLM loader node, it will automatically read the updated API key and Base URL from the `config.ini` file.
   - Starts a FastAPI service that can be used to call your ComfyUI workflow. If you run it directly, you get an OpenAI interface at `http://127.0.0.1:8817/v1/`. You need to connect the start and end of your workflow to the 'Start Workflow' and 'End Workflow', then save in API format to the `workflow_api` folder. Then, in any frontend that can call the OpenAI interface, input `model name=<your workflow name without the .json extension>`, `Base URL=http://127.0.0.1:8817/v1/`, and the API key can be filled with any value.
   - Starts a Streamlit application; the workflow saving process is as above. You can select your saved workflow in the 'Settings' of the Streamlit app and interact with your workflow agent in the 'Chat'.
   - 'About Us', which introduces this project.
2. The automatic model name list node has been removed and replaced with a simple API LLM loader node, which automatically retrieves your model name list from the configuration in your config.ini file. You just need to select a name to load the model. Additionally, the simple LLM loader, simple LLM-GGUF loader, simple VLM loader, simple VLM-GGUF loader, and simple LLM lora loader nodes have been updated. They all automatically read the model paths from the model folder within the party folder, making it easier for everyone to load various local models.
1. LLMs can now dynamically load lora like SD and FLUX. You can chain multiple loras to load more loras on the same LLM. Example workflow: [start_with_LLM_LORA](workflow/LLM_lora.json).
1. Added the [searxng](https://github.com/searxng/searxng) tool, which can aggregate searches across the entire web. Perplexica also relies on this aggregation search tool, so you can set up a Perplexica at your party. You can deploy the searxng/searxng public image in Docker, then start it using `docker run -d -p 8080:8080 searxng/searxng`, and access it using `http://localhost:8080`. You can fill in this URL `http://localhost:8080` in the party's searxng tool, and then you can use searxng as a tool for LLM.
1. **Major Update!!!** Now you can encapsulate any ComfyUI workflow into an LLM tool node. You can have your LLM control multiple ComfyUI workflows simultaneously. When you want it to complete some tasks, it can choose the appropriate ComfyUI workflow based on your prompt, complete your task, and return the result to you. Example workflow: [comfyui_workflows_tool](workflow/把任意workflow当作LLM_tool.json). The specific steps are as follows:
   - First, connect the text input interface of the workflow you want to encapsulate as a tool to the "user_prompt" output of the "Start Workflow" node. This is where the prompt passed in when the LLM calls the tool.
   - Connect the positions where you want to output text and images to the corresponding input positions of the "End Workflow" node.
   - Save this workflow as an API (you need to enable developer mode in the settings to see this button).
   - Save this workflow to the workflow_api folder of this project.
   - Restart ComfyUI and create a simple LLM workflow, such as: [start_with_LLM_api](workflow/start_with_LLM_api.json).
   - Add a "Workflow Tool" node to this LLM node and connect it to the tool input of the LLM node.
   - In the "Workflow Tool" node, write the name of the workflow file you want to call in the first input box, for example: draw.json. You can write multiple workflow file names. In the second input box, write the function of each workflow so that the LLM understands how to use these workflows.
   - Run it to see the LLM call your encapsulated workflow and return the result to you. If the return is an image, connect the "Preview Image" node to the image output of the LLM node to view the generated image. Note! This method calls a new ComfyUI on your 8190 port, please do not occupy this port. A new terminal will be opened on Windows and Mac systems, please do not close it. The Linux system uses the screen process to achieve this, when you do not need to use it, close this screen process, otherwise, it will always occupy your port.
   
![workflow_tool](img/workflowtool.png)

## User Guide
1. For the instructions for using the node, please refer to: [how to use nodes](https://github.com/heshengtao/Let-LLM-party)

2. If there are any issues with the plugin or you have other questions, feel free to join the QQ group: [931057213](img/Q群.jpg) | discord：[discord](https://discord.gg/f2dsAKKr2V).

3. Please refer to the workflow tutorial: [Workflow Tutorial](workflow_tutorial/), thanks to [HuangYuChuh](https://github.com/HuangYuChuh) for your contribution!

4. Advanced workflow gameplay account:[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

5. More workflows please refer to the [workflow](workflow) folder.

## Vedio tutorial
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## Model support
1. Support all API calls in openai format(Combined with [oneapi](https://github.com/songquanpeng/one-api) can call almost all LLM APIs, also supports all transit APIs), base_url selection reference [config.ini.example](config.ini.example), which has been tested so far:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (Perfectly compatible with all OpenAI models, including the 4o and o1 series!)
* [ollama](https://github.com/ollama/ollama) (Recommended! If you are calling locally, it is highly recommended to use the ollama method to host your local model!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (Recommended! If you want to use the local gguf format model, you can use the llama.cpp project's API to access this project!)
* [Grok](https://x.ai/api)
* [Tongyi Qianwen /qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [zhipu qingyan/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)

2. API calls that support Gemini format:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)

3. Compatible with most local models in the transformer library (the model type on the local LLM model chain node has been changed to LLM, VLM-GGUF, and LLM-GGUF, corresponding to directly loading LLM models, loading VLM models, and loading GGUF format LLM models). If your VLM or GGUF format LLM model reports an error, please download the latest version of llama-cpp-python from [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases). Currently tested models include:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay)(Recommended! Role-playing model)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)(Recommended! Rich prompt model)
* [meta-llama/llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)

4. Model download
* [Baidu cloud address](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), extraction code: qyhu

## Download
* You can configure the language in `config.ini`, currently only Chinese (zh_CN) and English (en_US), the default is your system language.
* Install using one of the following methods:
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
APIKEY can be configured using one of the following methods
### Method 1:
1. Open the `config.ini` file in the project folder of the `comfyui_LLM_party`.
2. Enter your openai_api_key, base_url in `config.ini`.
3. If you are using an ollama model, fill in `http://127.0.0.1:11434/v1/` in `base_url`, `ollama` in `openai_api_key`, and your model name in `model_name`, for example: `llama3`.
4. If you want to use Google search or Bing search tools, enter your `google_api_key`, `cse_id` or `bing_api_key` in `config.ini`.
5. If you want to use image input LLM, it is recommended to use image bed imgbb and enter your imgbb_api in `config.ini`.
6. Each model can be configured separately in the `config.ini` file, which can be filled in by referring to the `config.ini.example` file. After you configure it, just enter `model_name` on the node.


### Method 2:
1. Open the comfyui interface.
2. Create a Large Language Model (LLM) node and enter your openai_api_key and base_url directly in the node.
3. If you use the ollama model, use LLM_api node, fill in `http://127.0.0.1:11434/v1/` in `base_url` node, fill in `ollama` in `api_key`, and fill in your model name in `model_name`, for example: `llama3`.
4. If you want to use image input LLM, it is recommended to use graph bed imgbb and enter your `imgbb_api_key` on the node.

## Changelog
1. You can right-click in the comfyui interface, select `llm` from the context menu, and you will find the nodes for this project. [how to use nodes](https://github.com/heshengtao/Let-LLM-party)
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
11. Rapidly develop your own web applications using API + Streamlit.
12. Added a dangerous omnipotent interpreter node that allows the large model to perform any task.
13. It is recommended to use the `show_text` node under the `function` submenu of the right-click menu as the display output for the LLM node.
14. Supported the visual features of GPT-4O!sample workflow:[GPT-4o](workflow/GPT-4o.json)
15. A new workflow intermediary has been added, which allows your workflow to call other workflows!sample workflow:[Invoke another workflow](workflow/调用另一个工作流.json)
16. Adapted to all models with an interface similar to OpenAI, such as: Tongyi Qianwen/QWEN, Zhigu Qingyan/GLM, DeepSeek, Kimi/Moonshot. Please fill in the base_url, api_key, and model_name of these models into the LLM node to call them.
17. Added an LVM loader, now you can call the LVM model locally, support [lava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf) model, other LVM models should theoretically run if they are GGUF format.The example workflow can be found here: [start_with_LVM.json](workflow/start_with_LVM.json).
18. I wrote a `fastapi.py` file, and if you run it directly, you’ll get an OpenAI interface on `http://127.0.0.1:8817/v1/`. Any application that can call GPT can now invoke your comfyui workflow! I will create a tutorial to demonstrate the details on how to do this.
19. I’ve separated the LLM loader and the LLM chain, dividing the model loading and model configuration. This allows for sharing models across different LLM nodes!
20. macOS and mps devices are now supported! Thanks to [bigcat88](https://github.com/bigcat88) for their contribution!
21. You can build your own interactive novel game, and go to different endings according to the user's choice! Example workflow reference: [interactive_novel](workflow/互动小说.json)
22. Adapted to OpenAI's whisper and tts functions, voice input and output can be realized. Example workflow reference: [voice_input&voice_output](workflow/语音输入+语音输出.json)
23. Compatible with [Omost](https://github.com/lllyasviel/Omost)!!! Please download [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) to experience it now! Sample workflow reference: [start_with_OMOST](workflow/start_with_OMOST)
24. Added LLM tools to send messages to WeCom, DingTalk, and Feishu, as well as external functions to call.
25. Added a new text iterator, which can output only part of the characters at a time. It is safe to split the text according to Carriage Return and chunk size, and will not be divided from the middle of the text. chunk_overlap refers to how many characters the divided text overlaps. In this way, you can enter super long text in batches, as long as you don't have a brain to click, or open the loop in comfyui to execute, it can be automatically executed. Remember to turn on the is_locked property, which can automatically lock the workflow at the end of the input and will not continue to execute. Example workflow: [text iteration input](workflow/文本迭代输入.json)
26. Added the model name attribute to the local LLM loader, local llava loader. If it is empty, it will be loaded using various local paths in the node. If it is not empty, it will be loaded using the path parameters you fill in yourself in `config.ini`. If it is not empty and not in `config.ini`, it will be downloaded from huggingface or loaded from the model save directory of huggingface. If you want to download from huggingface, please fill in the format of for example: `THUDM/glm-4-9b-chat`.Attention! Models loaded in this way must be adapted to the transformer library.
27. Added JSON file parsing node and JSON value node, which allows you to get the value of a key from a file or text. Thanks to [guobalove](https://github.com/guobalove) for your contribution!
28. Improved the code of tool call. Now LLM without tool call function can also open is_tools_in_sys_prompt attribute (local LLM does not need to be opened by default, automatic adaptation). After opening, the tool information will be added to the system prompt word, so that LLM can call the tool.Related papers on implementation principles: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
29. A new custom_tool folder is created to store the code of the custom tool. You can refer to the code in the [custom_tool](custom_tool) folder, put the code of the custom tool into the custom_tool folder, and you can call the custom tool in LLM.
30. Added Knowledge Graph tool, so that LLM and Knowledge Graph can interact perfectly. LLM can modify Knowledge Graph according to your input, and can reason on Knowledge Graph to get the answers you need. Example workflow reference: [graphRAG_neo4j](workflow/graphRAG_neo4j.json)
31. Added personality AI function, 0 code to develop your own girlfriend AI or boyfriend AI, unlimited dialogue, permanent memory, stable personality. Example workflow reference: [Mylover Personality AI](workflow/麦洛薇人格AI.json)
32. You can use this LLM tool maker to automatically generate LLM tools, save the tool code you generated as a python file, and then copy the code to the custom_tool folder, and then you create a new node. Example workflow: [LLM tool generator](workflow/LLM工具制造机.json).
33. It supports duckduckgo search, but it has significant limitations. It seems that only English keywords can be entered, and multiple concepts cannot appear in keywords. The advantage is that there are no APIkey restrictions.
34. It supports the function of calling multiple knowledge bases separately, and it is possible to specify which knowledge base is used to answer questions in the prompt word. Example workflow: [multiple knowledge bases are called separately](workflow/多知识库分别调用.json).
35. Support LLM input extra parameters, including advanced parameters such as json out. Example workflow: [LLM input extra parameters](workflow/LLM额外参数eg_JSON_OUT.json).[Separate prompt words with json_out](workflow/用json_out分离提示词.json).
36. Added the function of connecting the agent to discord. (still testing)
37. Added the function of connecting the agent to Feishu, thank you very much [guobalove](https://github.com/guobalove) for your contribution! Refer to the workflow [Feishu robot](workflow/飞书机器人.json).
38. Added universal API call node and a large number of auxiliary nodes for constructing the request body and grabbing the information in the response.
39. Added empty model node, you can uninstall LLM from video memory at any location!
40. The [chatTTS](https://github.com/2noise/ChatTTS) node has been added, thank you very much for the contribution of [guobalove](https://github.com/guobalove)! `model_path` parameter can be empty! It is recommended to use `HF` mode to load the model, the model will be automatically downloaded from hugging face, no need to download manually; if using `local` loading, please put the model's`asset` and `config` folders in the root directory. [Baidu cloud address](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), extraction code: qyhu; if using `custom` mode to load, please put the model's `asset` and `config` folders under `model_path`.
2. Updated a series of conversion nodes: markdown to HTML, svg to image, HTML to image, mermaid to image, markdown to Excel.
1. Compatible with the llama3.2 vision model, supports multi-turn dialogue, visual functions. Model address: [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct). Example workflow: [llama3.2_vision](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json).
1. Adapted GOT-OCR2, supports formatted output results, supports fine text recognition using position boxes and colors. Model address: [GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0). Example workflow converts a screenshot of a webpage into HTML code and then opens the browser to display this webpage: [img2web](workflow/图片转网页.json).
2. The local LLM loader nodes have been significantly adjusted, so you no longer need to choose the model type yourself. The llava loader node and GGUF loader node have been re-added. The model type on the local LLM model chain node has been changed to LLM, VLM-GGUF, and LLM-GGUF, corresponding to directly loading LLM models, loading VLM models, and loading GGUF format LLM models. VLM models and GGUF format LLM models are now supported again. Local calls can now be compatible with more models! Example workflows: [LLM_local](workflow/start_with_LLM_local.json), [llava](workflow/start_with_llava.json), [GGUF](workflow/start_with_GGUF.json)
2. Added EasyOCR node for recognizing text and positions in images. It can generate corresponding masks and return a JSON string for LLM to view. There are standard and premium versions available for everyone to choose from!
2. In the comfyui LLM party, the strawberry system of the chatgpt-o1 series model was reproduced, referring to the prompts of [Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py). Example workflow: [Strawberry system compared to o1](workflow/草莓系统与o1对比.json).
2. A new GPT-sovits node has been added, allowing you to call the GPT-sovits model to convert text into speech based on your reference audio. You can also fill in the path of your fine-tuned model (if not filled, the base model will be used for inference) to get any desired voice. To use it, you need to download the [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS) project and the corresponding base model locally, then start the API service with `runtime\python.exe api_v2.py` in the GPT-sovits project folder. Additionally, the chatTTS node has been moved to [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia). The reason is that chatTTS has many dependencies, and its license on PyPi is CC BY-NC 4.0, which is a non-commercial license. Even though the chatTTS GitHub project is under the AGPL license, we moved the chatTTS node to comfyui LLM mafia to avoid unnecessary trouble. We hope everyone understands!
3. Now supports OpenAI’s latest model, the o1 series!
4. Added a local file control tool that allows the LLM to control files in your specified folder, such as reading, writing, appending, deleting, renaming, moving, and copying files.Due to the potential danger of this node, it is included in [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia).
5. New SQL tools allow LLM to query SQL databases.
6. Updated the multilingual version of the README. Workflow for translating the README document: [translate_readme](workflow/文档自动翻译机.json)
7. Updated 4 iterator nodes (text iterator, picture iterator, excel iterator, json iterator). The iterator modes are: sequential, random, and infinite. The order will be output in sequence until the index limit is exceeded, the process will be automatically aborted, and the index value will be reset to 0. Random will choose a random index output, and infinite will loop output.
8. Added Gemini API loader node, now compatible with Gemini official API!Since Gemini generates an error with a return code of 500 if the returned parameter contains Chinese characters during the tool call, some tool nodes are unavailable.example workflow:[start_with_gemini](workflow/start_with_gemini.json)
9. Added lore book node, you can insert your background settings when talking to LLM, example workflow: [lorebook](workflow/lorebook.json)
10. Added FLUX prompt word generator mask node, which can generate Hearthstone cards, Game King cards, posters, comics and other styles of prompt words, which can make the FLUX model straight out. Reference workflow: [FLUX prompt word](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## Next Steps Plan:
1. More model adaptations;
2. More ways to build agents;
3. More automation features;
4. More knowledge base management features;
5. More tools, more personas.

## Disclaimer:
This open-source project and its contents (hereinafter referred to as "Project") are provided for reference purposes only and do not imply any form of warranty, either expressed or implied. The contributors of the Project shall not be held responsible for the completeness, accuracy, reliability, or suitability of the Project. Any reliance you place on the Project is strictly at your own risk. In no event shall the contributors of the Project be liable for any indirect, special, or consequential damages or any damages whatsoever resulting from the use of the Project.

## Special thanks:
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## loan list 
Some of the nodes in this project have borrowed from the following projects. Thank you for your contributions to the open-source community!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## Support:

### Join the community
If there is a problem with the plugin or you have any other questions, please join our community.

1. discord:[discord link](https://discord.gg/f2dsAKKr2V)
2. QQ group: `931057213`

<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

3. WeChat group: `Choo-Yong` (enter the group after adding the small assistant WeChat)

### Follow us
1. If you want to continue to pay attention to the latest features of this project, please follow the Bilibili account: [Party host BB machine](https://space.bilibili.com/26978344)
2. The OpenArt account is continuously updated with the most useful party workflows:[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### Donation support
If my work has brought value to your day, consider fueling it with a coffee! Your support not only energizes the project but also warms the heart of the creator. ☕💖 Every cup makes a difference!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
