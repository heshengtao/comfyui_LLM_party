![图片](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">B站</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">文字教程</a> ·
  <a href="workflow_tutorial/">工作流教程</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">度盘链接</a> ·
  <a href="img/Q群.jpg">QQ群</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">关于我们</a>
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

C﻿​﻿‎﻿​﻿‎‏​﻿‍‎​﻿‎﻿​﻿‎‏​﻿‌‎​﻿‎‍​﻿‍‏​‍﻿‌​﻿‌‏omfyui_llm_party希望基于[comfyui](https://github.com/comfyanonymous/ComfyUI)这一个极为简约的UI界面作为前端，开发一套完整的用于LLM工作流搭建的节点库。可以让用户更便捷快速地搭建自己的LLM工作流，并且更方便地接入自己的图像工作流中。

## 效果展示
https://github.com/user-attachments/assets/9e627204-4626-479e-8806-cb06cd6157a6

## 项目综述

ComfyUI LLM Party，从最基础的 LLM 多工具调用、角色设定快速搭建自己的专属AI助手、到可以行业落地的词向量RAG、GraphRAG来本地化的管理行业内知识库；从单一的智能体流水线，到复杂的智能体与智能体辐射状交互模式、环形交互模式的构建;从个人用户需要的接入自己的社交APP(QQ、飞书、Discord)，到流媒体工作者需要的一站式LLM+TTS+ComfyUI工作流；从普通学生所需要的第一个LLM应用的简单上手起步，到科研工作者们常用的各类参数调试接口，模型适配。这一切，你都可以在ComfyUI LLM Party中找到答案。

## 快速开始
1. 直接将以下工作流拖入你的comfyui，然后用[comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager)安装缺失节点。
  - 使用API调用LLM：[start_with_LLM_api](workflow/start_with_LLM_api.json)
  - 使用ollama管理本地LLM：[start_with_Ollama](workflow/ollama.json)
  - 使用分散格式的本地LLM：[start_with_LLM_local](workflow/start_with_LLM_local.json)
  - 使用GGUF格式的本地LLM：[start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - 使用分散格式的本地VLM：[start_with_VLM_local](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json)（测试中，目前只支持[Llama-3.2-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)）
  - 使用GGUF格式的本地VLM：[start_with_VLM_GGUF](workflow/start_with_llava.json)
2. 如果你是使用API，在API LLM加载器节点上填入你的`base_url`（可以是中转API，注意结尾要用`/v1/`），例如：`https://api.openai.com/v1/` 以及`api_key`。
3. 如果你是使用ollama，在API LLM加载器节点上打开`is_ollama`选项，无需填写`base_url`和`api_key`。
4. 如果你是使用本地模型，在本地模型加载器节点上填入你的模型路径，例如：`E:\model\Llama-3.2-1B-Instruct`。也可以在本地模型加载器节点上填入hunggingface的模型repo id，例如：`lllyasviel/omost-llama-3-8b-4bits`。
5. 由于本项目有较高的使用门槛，所以即使你选择了快速开始，我也希望你能耐心阅读完本项目主页。

## 最新更新
1. fork了[chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)，新建了一个[party-on-wechat](https://github.com/heshengtao/party-on-wechat)，安装和使用方法与原项目一致，无需配置，只需要启动party的fastapi。默认是调用wx_api工作流，支持图片输出。后续会逐步更新，保证party在微信上的丝滑使用。
1. 添加了In-Context-LoRA面具节点，用于生成连续一致性的[In-Context-LoRA](https://github.com/ali-vilab/In-Context-LoRA/tree/main)提示词。
1. 添加了一个前端组件，从左到右的功能分别为：
  - 将你的API key和Base URL保存到config.ini文件，当你对API LLM加载器节点使用fix node后，他会自动读取config.ini文件中你修改后的API key和Base URL。
  - 启动一个fastapi，可以用来调用你的comfyui工作流，如果你直接运行它，你就获得了一个`http://127.0.0.1:8817/v1/`上的openai接口。你需要将你的工作流的开始和结尾连上开始工作流和结束工作流，然后以API格式保存到workflow_api文件夹，然后在其他可以调用openai接口的前端输入model name=<你的工作流名不包含.json后缀名>，Base URL=`http://127.0.0.1:8817/v1/`，API key随便填。
  - 启动一个streamlit应用，工作流保存流程如上，你可以在streamlit应用中的`设置`中选中你保存的工作流，并且在`聊天`中与你的工作流智能体聊天。
  - 关于我们，介绍本项目。
2. 移除了自动获取模型名称列表节点，取而代之的是简易API LLM加载器节点，自动从你的config.ini文件中的配置中获取你的模型名称列表，你只要选择一个名称就可以加载模型了。此外更新了简易LLM加载器、简易LLM-GGUF加载器、简易VLM加载器、简易VLM-GGUF加载器、简易LLM lora加载器节点。都是自动读取party文件夹的model文件夹内的模型路径，让大家更方便的加载各种本地模型。
3. 现在LLM可以像SD和FLUX一样动态加载lora了，你可以用多个lora串联，以在同一个LLM上加载多的lora。示例工作流：[start_with_LLM_LORA](workflow/LLM_lora.json)。
4. 添加了[searxng](https://github.com/searxng/searxng)工具，可以聚合搜索全网，Perplexica也是依赖于这个聚合搜索工具，相当于你可以在party里搭建一个Perplexica。你可以在docker中部署searxng/searxng公共镜像，然后使用`docker run -d -p 8080:8080 searxng/searxng`来启动它，然后使用`http://localhost:8080`来访问它。你可以将`http://localhost:8080`这个URL填入party的searxng工具，就可以将searxng当作LLM的一个工具使用了。
5. **超级重大更新！！！** 现在你可以将任意的comfyui工作流封装成一个LLM工具节点。你可以让你的LLM同时控制多个comfyui工作流，当你想要他完成一些任务时，他可以根据你的提示，选择合适的comfyui工作流，完成你的任务，并且将结果返回给你。示例工作流：[comfyui_workflows_tool](workflow/把任意workflow当作LLM_tool.json)。具体步骤如下：
  - 首先，将你待会需要被封装成工具的工作流的需要输入文字的接口连上“开始工作流”节点的“user_prompt”输出，这个位置是LLM调用工具时，传入的prompt。在你要输出文字和图片的位置连上“结束工作流”节点的对应输入位置。
  - 将这个工作流以API形式保存（需要再设置中开启开发者模式才能看到这个按钮）。
  - 将这个工作流保存到本项目的workflow_api文件夹中。
  - 重启comfyui，建立一个简单的LLM工作流，例如：[start_with_LLM_api](workflow/start_with_LLM_api.json)。
  - 给这个LLM节点添加一个“工作流工具”节点，连在LLM节点的tool输入上。
  - 在“工作流工具”节点上，在第一个输入框中写入想要调用的工作流文件名，例如：draw.json，可以写入多个工作流文件名。在第二个输入框中写入每个工作流的作用，这样可以让LLM明白这些工作流怎么用。
  - 运行即可看到这个LLM调用你封装好的工作流，并且将结果返回给你。如果返回的是图片，请在LLM节点的image输出上连上“预览图片”节点，查看生成的图片。注意！该方法是在你的8190端口调用了一个新的comfyui，请不要占用这个端口。window和mac系统会有一个新的终端被打开，请不要关闭。Linux系统使用的是screen进程实现的，当你不需要用时，关闭这个screen进程，否则会一直占用你的端口。
  
![workflow_tool](img/workflowtool.png)

## 使用说明
1. 节点的使用说明请参考：[怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. 如果插件存在问题或者您有其他的疑问，欢迎加入QQ群：[931057213](img/Q群.jpg) | discord：[discord](https://discord.gg/f2dsAKKr2V)

3. 工作流教程请参考：[工作流教程](workflow_tutorial/)，感谢[HuangYuChuh](https://github.com/HuangYuChuh)的贡献！

4. 高阶工作流玩法账号：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. 更多的工作流可以参考[workflow](workflow)文件夹

## 视频教程
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## 模型支持
1. 支持所有openai格式的API调用(结合[oneapi](https://github.com/songquanpeng/one-api)可以调用几乎所有LLM API，也支持所有的中转API)，base_url的选择参考[config.ini.example](config.ini.example)，目前已测试的有：
* [openai](https://platform.openai.com/docs/api-reference/chat/create)（完美适配所有的openai模型，包括4o和o1系列！）
* [ollama](https://github.com/ollama/ollama)（推荐！如果你是本地调用，非常推荐使用ollama方式托管你的本地模型！）
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server)（推荐！如果你想使用本地gguf格式的模型，可以使用llama.cpp项目的API接入本项目！）
* [Grok](https://x.ai/api)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [豆包](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)

2. 支持Gemini格式的API调用：
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)

3. 兼容transformer库的大部分本地模型（本地LLM模型链节点上的model type已改成LLM、VLM-GGUF、LLM-GGUF三个选项，对应了直接加载LLM模型、加载VLM模型和加载GGUF格式的LLM模型），如果你的VLM或GGUF格式的LLM模型报错了，请在[llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases)下载最新版本的llama-cpp-python，目前已测试的有：
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay)(推荐！角色扮演模型)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)(推荐！丰富提示词模型)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)

4. 模型下载：
* [百度云地址](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)，提取码：qyhu

## 下载
使用以下方法之一安装
### 方法一：
1. 在[comfyui管理器](https://github.com/ltdrdata/ComfyUI-Manager)中搜索`comfyui_LLM_party`，一键安装
2. 重启comfyui

### 方法二：
1. 导航到 ComfyUI 根文件夹中下的`custom_nodes`子文件夹
2. 使用克隆此存储库。`git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### 方法三：
1. 点击右上角的`CODE`
2. 点击`download zip`
3. 将下载的压缩包解压到ComfyUI 根文件夹中下的`custom_nodes`子文件夹中

## 环境部署
1. 导航到`comfyui_LLM_party`的项目文件夹
2. 在终端输入`pip install -r requirements.txt`将本项目需要的第三方库部署到comfyui的环境中。请注意你是否在comfyui的环境进行安装，并关注终端中的`pip`报错
3. 如果你是用的comfyui启动器，你需要在终端中输入 `启动器配置中的路径\python_embeded\python.exe -m pip install -r requirements.txt`进行安装。`python_embeded`文件夹一般与你的`ComfyUI`文件夹同级。
4. 如果你出现了一些环境配置问题，可以尝试使用`requirements_fixed.txt`中的依赖。

## 配置
* 可以在`config.ini`中配置语言，目前只有中文（zh_CN）和英文（en_US）两种，默认为你的系统语言。
* 可以使用以下方法之一配置APIKEY
### 方法一：
1. 打开`comfyui_LLM_party`的项目文件夹下的`config.ini`文件。
2. 在`config.ini`输入你的`openai_api_key`、`base_url`。
3. 如果你使用ollama模型，在`base_url`填入`http://127.0.0.1:11434/v1/`，在`openai_api_key`填入`ollama`，在`model_name`填入你的模型名称，例如:llama3。
4. 如果你要使用谷歌搜索或者必应搜索工具，在`config.ini`输入你的`google_api_key`、`cse_id`或`bing_api_key`。
5. 如果你要使用图片输入LLM，推荐使用图床imgbb，在`config.ini`输入你的`imgbb_api`。
6. 每个模型都可以在`config.ini`文件中单独配置，可以参考`config.ini.example`文件填写。当你配置好之后，只需要在节点上输入`model_name`即可。

### 方法二：
1. 打开comfyui界面。
2. 新建大语言模型（LLM）节点，在节点中直接输入你的`openai_api_key`、`base_url`。
3. 如果你使用ollama模型，请使用LLM_api节点，在节点的`base_url`填入`http://127.0.0.1:11434/v1/`，在`api_key`填入`ollama`，在`model_name`填入你的模型名称，例如:llama3。。
4. 如果你要使用图片输入LLM，推荐使用图床imgbb，在节点上输入你的`imgbb_api_key`。

## 更新日志
1. 你可以在comfyui界面里点击右键，选择右键菜单里的`llm`，即可找到本项目的节点。[怎么使用节点](https://github.com/heshengtao/Let-LLM-party)
2. 支持API接入或者本地大模型接入。模块化实现工具调用功能。在填入base_url时，请填入以`/v1/`结尾的网址。你可以用[ollama](https://github.com/ollama/ollama)来管理你的模型，然后在base_url填入`http://127.0.0.1:11434/v1/`，在api_key填入ollama，在model_name填入你的模型名称，例如:llama3。
- API接入示例工作流：[start_with_LLM_api](workflow/start_with_LLM_api.json)
- 本地模型接入示例工作流：[start_with_LLM_local](workflow/start_with_LLM_local.json)
- ollama接入示例工作流：[ollama](workflow/ollama.json)
3. 本地知识库接入，支持RAG。示例工作流：[知识库RAG搜索.json](workflow/知识库RAG搜索.json)
4. 可以调用代码解释器
5. 可以联网查询，支持谷歌搜索。示例工作流：[电影查询工作流](workflow/电影查询工作流.json)
6. 可以在comfyui中实现条件语句，可以对用户提问进行分类后再针对性回复。示例工作流：[智能客服](workflow/智能客服.json)
7. 支持大模型的回环链接，可以让两个大模型打辩论赛。示例工作流：[电车难题辩论赛](workflow/电车难题辩论赛.json)
8. 支持挂接任意人格面具，可以自定义提示词模板
9. 支持多种工具调用，目前开发了查天气、查时间、知识库、代码执行、联网搜索、对单一网页进行搜索等功能。
10. 支持将LLM当作一个工具节点使用。示例工作流：[LLM套娃](workflow/LLM套娃.json)
11. 支持通过API+streamlit快速开发自己的web应用。
12. 新增了危险的万能解释器节点，可以让大模型做任何事情
13. 推荐使用右键菜单里的函数（function）子目录下的显示文本（show_text）节点，作为LLM节点的输出显示
14. 支持了GPT-4O的视觉功能！示例工作流：[GPT-4o](workflow/GPT-4o.json)
15. 新增了一个工作流中转器，可以让你的工作流调用其他的工作流!示例工作流：[调用另一个工作流](workflow/调用另一个工作流.json)
16. 适配了所有具有类似openai接口的模型，例如：通义千问/qwen、智谱清言/GLM、deepseek、kimi/moonshot。请将这些模型的base_url、api_key、model_name填入LLM节点以调用它们。
17. 新增了一个LVM加载器，现在可以本地调用LVM模型了，支持[llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)模型，其他LVM模型如果是GGUF格式，理论上应该也可以运行。示例工作流在这里: [start_with_LVM.json](workflow/start_with_LVM.json).
18. 写了一个`fastapi.py`文件，如果你直接运行它，你就获得了一个`http://127.0.0.1:8817/v1/`上的openai接口，任何可以调用GPT的应用都可以调用你的comfyui工作流了！详细怎么操作我会出一期教程来演示~
19. 拆分了LLM加载器和LLM链，把模型加载和模型设置分开来了，这样就可以在不同的LLM节点之间共享模型了!
20. 目前已经支持了macOS以及mps设备!感谢[bigcat88](https://github.com/bigcat88)对此的贡献！
21. 可以搭建自己的互动小说游戏了，根据用户的选择，走向不同的结局！示例工作流参考：[互动小说](workflow/互动小说.json)
22. 适配了openai的whisper和tts功能，可以实现语音输入和输出。示例工作流参考：[语音输入+语音输出](workflow/语音输入+语音输出.json)
23. 兼容[Omost](https://github.com/lllyasviel/Omost)啦！！！请下载[omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)立即体验吧！示例工作流参考：[start_with_OMOST](workflow/start_with_OMOST.json)
24. 新增了将消息发送到企业微信、钉钉和飞书的LLM工具以及可供调用的外部函数。
25. 新增了一个文本迭代器，可以每次只输出一部分的字符，是根据回车符号和chunk size来安全分割文本的，不会从文本中间分割。chunk_overlap是指分割的文本重叠多少字符。这样可以批量输入超长文本，只要无脑点击，或者开启comfyui里的循环执行就行了，就可以自动执行完了。记得开启is_locked属性，可以在输入结束时，自动锁住工作流，不会继续执行。示例工作流：[文本迭代输入](workflow/文本迭代输入.json)
26. 在本地LLM加载器、本地llava加载器上添加了model name属性，如果为空，则使用节点中的各类本地path加载。如果不为空，则会使用`config.ini`中你自己填写的路径参数加载。如果不为空且不在`config.ini`中，则会从huggingface上下载或则从huggingface的模型保存目录中加载。如果你想从huggingface上下载，请按照例如：`THUDM/glm-4-9b-chat`的格式填写model name属性。注意！这样子加载的模型必须适配transformer库。
27. 新增了JSON文件解析节点和JSON取值节点，可以让你从文件或者文本中获取某一个键的值。感谢[guobalove](https://github.com/guobalove)的贡献！
28. 改进了工具调用的代码，现在没有工具调用功能的LLM也可以开启is_tools_in_sys_prompt属性（本地LLM默认无需开启，自动适配），开启之后，工具信息会添加到系统提示词中，这样LLM就可以调用工具了。实现原理的相关论文：[Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
29. 新建了custom_tool文件夹，用于存放自定义工具的代码，可以参考[custom_tool](custom_tool)文件夹中的代码，将自定义工具的代码放入custom_tool文件夹中，即可在LLM中调用自定义工具。
30. 新增了知识图谱工具，让LLM与知识图谱可以完美交互，LLM可以根据你的输入修改知识图谱，可以在知识图谱上推理以获取你需要的答案。示例工作流参考：[graphRAG_neo4j](workflow/graphRAG_neo4j.json)
31. 新增了人格AI功能，0代码开发自己的女友AI或男友AI，无限对话，永久记忆，人设稳定。示例工作流参考：[麦洛薇人格AI](workflow/麦洛薇人格AI.json)
32. 可以使用这个LLM工具制造机自动生成LLM工具，把你生成的工具代码保存为一个python文件中，然后把代码复制到custom_tool文件夹下，然后你就创造了一个新的节点。示例工作流：[LLM工具生成器](workflow/LLM工具制造机.json)。
33. 支持了duckduckgo搜索，但是有很大的限制，似乎只能输入英文关键词，关键词也不能出现多个概念，优势在于没有任何APIkey的限制。
34. 支持了多个知识库分开调用的功能，可以在提示词内明确是使用哪个知识库的知识回答问题。示例工作流：[多知识库分别调用](workflow/多知识库分别调用.json)。
35. 支持LLM输入额外参数，包括json out等高级参数。示例工作流：[LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json)。[用json_out分离提示词](workflow/用json_out分离提示词.json)。
36. 新增将智能体接入discord的功能。(还在测试中)
37. 新增将智能体接入飞书的功能，超级感谢[guobalove](https://github.com/guobalove)的贡献！参考工作流
[飞书机器人](workflow/飞书机器人.json)。
38. 新增了万能API调用节点以及大量的辅助节点，用于构造请求体和抓取响应中的信息。
39. 新增了清空模型节点，可以在任意位置将LLM从显存中卸载！
40. 已添加了[chatTTS](https://github.com/2noise/ChatTTS)节点，超级感谢[guobalove](https://github.com/guobalove)的贡献！`model_path`参数可以为空！推荐使用HF模式加载模型，模型会自动从hugging face上下载，无需手动下载；如果使用local加载，请将模型的`asset`和`config`文件夹放到根目录下。[百度云地址](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)，提取码：qyhu；如果使用`custom`模式加载，请将模型的`asset`和`config`文件夹放到`model_path`下。
2. 更新了一系列转换节点，markdown转HTML，svg转图片，HTML转图片，mermaid转图片，markdown转Excel。
1. 兼容了llama3.2 vision模型，支持多轮对话，视觉功能,模型地址：[meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)，示例工作流：[llama3.2_vision](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json)
2. 适配了GOT-OCR2，支持格式化输出结果，支持使用位置box和颜色来精细识别文字，模型地址：[GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0),示例工作流将一张网页的截图转换成了HTML代码再打开浏览器显示这个网页：[img2web](workflow/图片转网页.json)
2. 大幅调整了本地LLM加载器节点，不用自己选择model type了。重新添加了llava加载器节点和GGUF加载器节点。本地LLM模型链节点上的model type已改成LLM、VLM-GGUF、LLM-GGUF三个选项，对应了直接加载LLM模型、加载VLM模型和加载GGUF格式的LLM模型。重新支持了VLM模型和GGUF格式的LLM模型。现在本地调用可以兼容更多的模型了！示例工作流：[LLM_local](workflow/start_with_LLM_local.json)，[llava](workflow/start_with_llava.json)，[GGUF](workflow/start_with_GGUF.json)
2. 已加入easyOCR节点，用于识别图中文字和位置，可以生成对应的mask，可以返回一个json字符串供LLM查看，有普通版本和高级版本供大家选择！
2. 在comfyui LLM party中复现了chatgpt-o1系列模型的草莓系统，参考了[Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py)的提示词，示例工作流：[Strawberry system compared to o1](workflow/草莓系统与o1对比.json)。
2. 新增了GPT-sovits节点，可以调用GPT-sovits模型，将文字根据你的参考音频转换为语音，也可以将你微调后的模型路径填入（如果不填就是基底模型进行推理），获得你想要的任意音色。使用时，需要下载[GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS)项目和对应的基底模型到本地，然后在GPT-sovits项目文件夹下用`runtime\python.exe api_v2.py`启动API服务。此外，chatTTS节点被移动到了[comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)中。原因是chatTTS的依赖库较多，且在PyPi中的许可证为CC BY-NC 4.0，这是一个非商用许可证。即使chatTTS的github项目是AGPL协议的，我们还是为了避免不必要的麻烦，将chatTTS节点移到了comfyui LLM mafia中。希望大家能够理解！
3. 现已支持openai最新模型o1系列模型!!!!
4. 新增了本地文件控制工具，让LLM可以控制你指定的文件夹的文件，例如：读取、写入、追加、删除、重命名、移动、复制文件等。由于该节点比较危险，收录在[comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)中。
5. 新增SQL工具，可以让LLM查询SQL数据库。
6. 更新了readme的多语言版本，翻译readme文档的工作流：[translate_readme](workflow/文档自动翻译机.json)
7. 更新了4个迭代器节点（文字迭代器、图片迭代器、表格迭代器、json迭代器），迭代器模式有：顺序、随机和无限三种模式。顺序会按顺序依次输出，直到超出索引上限自动中止进程，并将索引值重置为0，随机会选择一个随机索引输出，无限会无限循环输出。
8. 新增了Gemini API加载器节点，现在兼容Gemini官方的API啦！如果你是国内网络环境，如果出现API地区受限制的问题，请将节点切换到美国，并使用TUN模式。由于Gemini在工具调用时，如果返回的参数中包含中文字符会出现返回码为500的报错，因此部分工具节点不可用。示例工作流：[start_with_gemini](workflow/start_with_gemini.json)
9. 新增lore book节点，可以在与LLM对话时插入你的背景设定，示例工作流：[lorebook](workflow/lorebook.json)
10. 新增了FLUX提示词生成器面具节点，可以生成炉石卡牌、游戏王卡牌、海报、漫画等多种风格的提示词，可以让FLUX模型直出。参考工作流：[FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## 下一步计划：
1. 更多的模型适配；
2. 更多的智能体的搭建方式。
3. 更多的自动化功能。
4. 更多的知识库管理功能。
5. 更多的工具、更多的人格面具。

## 免责声明：
本开源项目及其内容（以下简称“项目”）仅供参考之用，并不意味着任何明示或暗示的保证。项目贡献者不对项目的完整性、准确性、可靠性或适用性承担任何责任。任何依赖项目内容的行为均需自行承担风险。在任何情况下，项目贡献者均不对因使用项目内容而产生的任何间接、特殊或附带的损失或损害承担责任。

## 特别感谢
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

## 借物表
本项目中的一些节点借鉴了以下项目，感谢他们在开源社区中的贡献！
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## 支持：

### 加入社群
如果插件存在问题或者您有其他的疑问，欢迎加入我们的社群。

1. QQ群：`931057213`

<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. 微信群：`Choo-Yong`（添加小助手微信后进群）

3. discord:[discord链接](https://discord.gg/f2dsAKKr2V)

### 关注我们
1. 如果想持续关注本项目的最新功能，欢迎关注B站账号：[派对主持BB机](https://space.bilibili.com/26978344)
2. OpenArt账号持续更新最有用的party工作流：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### 捐赠支持
如果我的工作给您带来了价值，请考虑请我喝一杯咖啡吧！您的支持不仅为项目注入活力，也温暖了创作者的心。☕💖 每一杯都有意义！
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## 星标历史

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
