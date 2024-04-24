<p align="right">
   <strong>中文</strong> | <a href="./README.md">English</a>
</p>

## 最新更新
1. 新增了start_workflow和end_workflow节点，你可以用这个两个节点来定义工作流的起点和终点，将你的工作流放到本项目文件夹下的workflow子文件夹，然后在本项目文件夹下点击setup_streamlit_app.bat，在streamlit的界面中，点击设置，替换为你的工作流，** 恭喜你，你构建了一个智能应用！ **你可以使用测试画画app这个工作流，测试该流程。请在测试前确保该工作流中的所有模型可以正常使用。
2. 支持GPT4的视觉功能，可以读取comfyui中的图片，但需要配合免费的图片托管服务imgbb实现这一功能。
3. 新增了面具节点，你可以快速启用你设定好的系统词，或者使用自定义面具，快速调整提示词模板
4. 实现了在comfyui中的条件语句，可以让大模型在判断后输出给后续不同的接口
5. 增加了更多的示例工作流，欢迎大家直接使用！

# **COMFYUI LLM PARTY——面向comfyui开发的LLM工具节点库** 

## 简介
[comfyui](https://github.com/comfyanonymous/ComfyUI)是一个极为简约的UI界面，主要用于AI绘图等基于SD模型的工作流搭建。本项目希望基于comfyui开发一套完整的用于LLM工作流搭建的节点库。可以让用户更便捷快速地搭建自己的LLM工作流，并且更方便地接入自己的SD工作流中。（图为由本项目节点搭建的智能客服工作流。更多示例工作流请在[workflow](workflow/)文件夹中查看。）

![图片](img/智能助手.png)

## 使用说明
[【ComfyUI×LLM】手把手教你如何搭建积木化智能体（超简单！）](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

## 特征
1. 你可以在comfyui界面里点击右键，选择右键菜单里的`llm`，即可找到本项目的节点。[怎么使用节点](how_to_use_nodes_ZH.md)
2. 支持openai的API驱动，并支持自定义base_url，可以使用中转API驱动LLM节点。如果你使用的是其他的大模型接口，可以使用[openai-style-api](https://github.com/tian-minghui/openai-style-api)转化成openai接口格式。本地大模型请选择本地大模型节点，目前适配了GLM和llama，但是llama不能使用工具调用，因为原生llama并不包含这个功能
3. 本地知识库接入，支持RAG
4. 可以调用代码解释器
5. 可以联网查询，支持谷歌搜索
6. 可以在comfyui中实现条件语句，可以对用户提问进行分类后再针对性回复
7. 支持大模型的回环链接，可以让两个大模型打辩论赛
8. 支持挂接任意人格面具，可以自定义提示词模板
9. 支持多种工具调用，目前开发了查天气、查时间、知识库、代码执行、联网搜索、对单一网页进行搜索等功能，未来还有更多的工具在开发中
10. 推荐配合[ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)的show_text节点，作为LLM节点的输出显示

## 下载
[百度云下载](https://pan.baidu.com/s/13ogn1np6bHgxOJhS--QJmg?pwd=jppj) （推荐！包含一个环境配置完毕且包含本项目的comfyui压缩包和一个本项目文件夹，前者下载完后不用再配置环境！）

或使用以下方法之一安装
### 方法一：
1. 在[comfyui管理器](https://github.com/ltdrdata/ComfyUI-Manager)中搜索`comfyui_LLM_party`，一键安装
2. 重启comfyui。

### 方法二：
1. 导航到 ComfyUI 根文件夹中下的`custom_nodes`子文件夹
2. 使用`git clone https://github.com/heshengtao/comfyui_LLM_party.git`克隆此存储库。

### 方法三：
1. 点击右上角的`CODE`
2. 点击`download zip`
3. 将下载的压缩包解压到ComfyUI 根文件夹中下的`custom_nodes`子文件夹中

## 环境部署
1. 导航到`comfyui_LLM_party`的项目文件夹
2. 在终端输入`pip install -r requirements.txt`将本项目需要的第三方库部署到comfyui的环境中。请注意你是否在comfyui的环境进行安装，并关注终端中的`pip`报错
3. 如果你是用的comfyui启动器，你需要在终端中输入 `启动器配置中的路径\python_embeded\python.exe 启动器配置中的路径\python_embeded\Scripts\pip.exe  install -r requirements.txt`进行安装。`python_embeded`文件夹一般与你的`ComfyUI`文件夹同级。

## 配置
可以使用以下方法之一配置APIKEY
### 方法一：
1. 打开`comfyui_LLM_party`的项目文件夹下的`config.ini`文件
2. 在`config.ini`输入你的`openai_api_key`、`base_url`
3. 如果你要使用谷歌搜索工具，在`config.ini`输入你的`google_api_key`、`cse_id`

### 方法二：
1. 打开comfyui界面
2. 新建大语言模型（LLM）节点，在节点中直接输入你的`openai_api_key`、`base_url`
3. 新建谷歌搜索工具（google_tool）节点，在节点中直接输入你的`google_api_key`、`cse_id`

## 下一步计划：
1. 更多的常用工具节点，比如：代码解释器、文字转语音输出、识别图中文字信息等等
2. 让LLM可以内部调用一个附属于它的LLM，让助手也有自己的助手。
3. 更多可以与comfyui中的大量SD节点进行连接的新节点，让LLM与SD有更多的可能，并提供相关的工作流

## 如果我的工作给您带来了价值，请考虑请我喝一杯咖啡吧！您的支持不仅为项目注入活力，也温暖了创作者的心。☕💖 每一杯都有意义！
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>
