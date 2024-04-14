# **COMFYUI LLM PARTY—A Node Library for LLM Workflow Development in ComfyUI** 

## Introduction
[comfyui](https://github.com/comfyanonymous/ComfyUI)is an extremely minimalist UI interface, primarily used for AI drawing and other workflows based on the SD model. This project aims to develop a complete set of nodes for LLM workflow construction based on comfyui. It allows users to quickly and conveniently build their own LLM workflows and easily integrate them into their existing SD workflows.

## Features
1. This project includes the following nodes:
   - “LLM”: “Large Language Model (LLM)”
   - “load_file”: “Load files from comfyui_LLM_party/file”
   - “tool_combine”: “Tool Combine”
   - “tool_combine_plus”: “Super Tool Combine”
   - “time_tool”: “Time Tool”
   - “weather_tool”: “Weather Tool”
   - “google_tool”: “Google Search Tool”
   - “check_web_tool”: “Check Web Tool”
   - “file_combine”: “File Combine”
   - “file_combine_plus”: “Super File Combine”
   - “start_dialog”: “Start Dialogue”
   - “end_dialog”: “End Dialogue”
2. Supports OpenAI API driving and custom base_url, allowing the use of a proxy API to drive LLM nodes.
3. Supports importing various file types into LLM nodes. With RAG technology, LLM can answer questions based on file content. Currently supported file types include: .docx, .xlsx, .csv, .txt, .py, .js, .java, .c, .cpp, .html, .css, .sql, .r, .swift
4. The tool combine node allows multiple tools to be passed into the LLM node, and the file combine node allows multiple files to be passed into the LLM node.
5. Supports Google search and single web page search, enabling LLM to perform online queries.
6. Through the start_dialog node and the end_dialog node, a loopback link can be established between two LLMs, meaning the two LLMs act as each other’s input and output!

## Download
[Baidu Cloud Download](https://pan.baidu.com/s/13ogn1np6bHgxOJhS--QJmg?pwd=jppj) 

Or install using one of the following methods:
### Method One:
1. Navigate to the `custom_nodes` subfolder under the ComfyUI root folder.
2. Clone this repository with `git clone https://github.com/heshengtao/comfyui_LLM_party.git`.

### Method Two:
1. Click `CODE` in the upper right corner.
2. Click `download zip`.
3. Unzip the downloaded package into the `custom_nodes` subfolder under the ComfyUI root folder.

## Environment Deployment
1. Navigate to the `comfyui_LLM_party` project folder.
2. Enter `pip install -r requirements.txt` in the terminal to deploy the third-party libraries required by the project into the comfyui environment. Please ensure you are installing within the comfyui environment and pay attention to any `pip` errors in the terminal.
3. If you are using the comfyui launcher, you need to enter `path_in_launcher_configuration\python_embeded\python.exe path_in_launcher_configuration\python_embeded\Scripts\pip.exe install -r requirements.txt` in the terminal to install. The `python_embeded` folder is usually at the same level as your `ComfyUI` folder.

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

## If my work has helped you, please buy me a coffee~~
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>
