import io
import json
import os
import time
import urllib.parse
import urllib.request
import uuid

import pandas as pd
import pygments
import streamlit as st
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
from PIL import Image
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


def get_all(ws, prompt):
    prompt_id = queue_prompt(prompt)["prompt_id"]
    output_images = {}
    output_text = ""
    while True:
        try:
            history = get_history(prompt_id)[prompt_id]
            break
        except Exception:
            time.sleep(0.1)
            continue
    for o in history["outputs"]:
        for node_id in history["outputs"]:
            node_output = history["outputs"][node_id]
            if "images" in node_output:
                images_output = []
                for image in node_output["images"]:
                    image_data = get_image(image["filename"], image["subfolder"], image["type"])
                    images_output.append(image_data)
                output_images[node_id] = images_output
            if "response" in node_output:
                output_text = node_output["response"][0]["content"]

    return output_images, output_text


def api(
    file_content="",
    image_input=None,
    file_path="",
    img_path="",
    system_prompt="你是一个强大的智能助手",
    user_prompt="",
    positive_prompt="",
    negative_prompt="",
    model_name="",
    workflow_path="fastapi.json",
):
    global current_dir_path
    workflow_path = workflow_path
    WF_path = os.path.join(current_dir_path, "workflow_api", workflow_path)
    with open(WF_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt = json.loads(prompt_text)

    for p in prompt:
        # 如果p的class_type是start_workflow
        if prompt[p]["class_type"] == "start_workflow":
            if file_content != "":
                prompt[p]["inputs"]["file_content"] = file_content
            if image_input is not None and image_input != []:
                prompt[p]["inputs"]["image_input"] = image_input
            prompt[p]["inputs"]["file_path"] = file_path
            prompt[p]["inputs"]["img_path1"] = img_path
            prompt[p]["inputs"]["system_prompt"] = system_prompt
            prompt[p]["inputs"]["user_prompt"] = user_prompt
            prompt[p]["inputs"]["positive_prompt"] = positive_prompt
            prompt[p]["inputs"]["negative_prompt"] = negative_prompt
            prompt[p]["inputs"]["model_name"] = model_name

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images, res = get_all(ws, prompt)
    return images, res


#####以下是UI界面部分代码，上面是API接口代码

button_style = """
<style>
div.stButton > button:first-child {
    background-color: white; /* White background */
    color: black; /* Black text */
    width: 100%; /* Full width */
    border: 1px solid #ccc; /* Light grey border */
    padding: 10px 24px; /* Padding */
    border-radius: 4px; /* Rounded corners */
    transition: background-color 0.3s, color 0.3s; /* Smooth transition */
}

div.stButton > button:first-child:hover {
    background-color: #d2d1d1; /* Very light background on hover */
    color: black; /* Black text on hover */
}

div.stButton > button:first-child:active {
    background-color: #bababa; /* Light background on click */
}

div[data-testid="stForm"] {
    border: none !important; /* 隐藏边框 */
    padding: 0 !important; /* 移除内边距 */
    margin: 0 !important; /* 移除外边距 */
}

/* 隐藏 text_area 的标签 */
div.stTextArea > label {
    display: none;
}

/* 当 text_area 获得焦点时，设置边框颜色为橙色 */
div.stTextArea textarea:focus {
    border-color: #FFA500;
    box-shadow: 0 0 0.25rem rgba(255, 165, 0, 0.5); /* 可选：添加发光效果 */
}
</style>
"""

# Add the custom button style to the Streamlit app
st.markdown(button_style, unsafe_allow_html=True)


language_mapping = {
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".r": "r",
    ".swift": "swift",
    # Add more mappings for other languages as needed
}
# 如果没有'wf_path'就创造
if "wf_path" not in st.session_state:
    st.session_state["wf_path"] = "fastapi.json"
# 如果没有'system_prompt'就创造
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = "你是一个强大的智能助手"


def get_current_page():
    # 安全地获取当前页面
    return st.session_state.get("current_page", "chat")  # 默认返回 'chat'


def set_current_page(page_name):
    # 安全地设置当前页面
    st.session_state["current_page"] = page_name


# 初始化当前页面的会话状态（如果尚未设置）
set_current_page(get_current_page())
current_dir_path = os.path.dirname(os.path.realpath(__file__))
# 创建侧边栏按钮
if st.sidebar.button("聊天"):
    set_current_page("chat")
if st.sidebar.button("设置"):
    set_current_page("settings")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
# 使用函数来访问 'current_page'
if get_current_page() == "chat":
    response = "你好哇~"
    ai_name = st.session_state["wf_path"]
    ai_name = ai_name.replace(".json", "")
    st.markdown(f"{ai_name}: 你好哇~")
    chat_history_container = st.container()  # Use a container to hold the chat history
    # 更新对话记录容器
    chat_history_container.empty()

    def display_chat_history():
        # 更新对话记录容器
        chat_history_container.empty()
        with chat_history_container:
            for message in st.session_state["chat_history"]:
                if message["role"] == "assistant":
                    if message["content"] is not None and message["content"] != "" and message["content"] != "empty":
                        st.markdown(f"{ai_name}: {message['content']}")
                elif message["role"] == "user":
                    st.markdown(f"你: {message['content']}")
                elif message["role"] == "image":
                    if message["content"] is not None:
                        st.markdown(f"{ai_name}:")
                        st.image(message["content"])

    with st.form("Question", clear_on_submit=True):
        # 用户输入
        user_input = st.text_area("", height=100, placeholder="让我们开始聊天吧...")
        # 文件上传
        uploaded_file = st.file_uploader(
            "上传文件或图片",
            type=[
                "png",
                "jpg",
                "jpeg",
                "txt",
                "docx",
                "doc",
                "pdf",
                "xlsx",
                "xls",
                "csv",
                "py",
                "html",
                "css",
                "sql",
                "r",
                "swift",
                "javascript",
                "java",
                "c",
                "cpp",
            ],
        )
        col3, col4 = st.columns(2)
        with col3:
            if st.form_submit_button("发送"):
                st.session_state["chat_history"].append({"role": "user", "content": user_input})
                file_path = ""
                img_path = ""
                if uploaded_file is not None:
                    # 如果上传的是照片，将文件路径传入image_path变量，否则传入file_path变量
                    if uploaded_file.type.startswith("image"):
                        # 保存上传的文件
                        with open(os.path.join(current_dir_path, "img", uploaded_file.name), "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        img_path = os.path.join(current_dir_path, "img", uploaded_file.name)
                        file_path = ""
                        st.session_state["chat_history"].append({"role": "image", "content": uploaded_file})
                    else:
                        # 保存上传的文件
                        with open(os.path.join(current_dir_path, "file", uploaded_file.name), "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        file_path = os.path.join(current_dir_path, "file", uploaded_file.name)
                        img_path = ""
                # 调用API函数
                images, response = api(
                    "",
                    None,
                    file_path,
                    img_path,
                    st.session_state["system_prompt"],
                    user_input,
                    positive_prompt="",
                    negative_prompt="",
                    model_name="",
                    workflow_path=str(st.session_state["wf_path"]),
                )
                # 更新对话记录
                if response is not None and response != "" and response != "empty":
                    st.session_state["chat_history"].append({"role": "assistant", "content": response})
                if images is not None:
                    # 更新对话记录
                    for node_id in images:
                        for image_data in images[node_id]:
                            image = Image.open(io.BytesIO(image_data))
                            st.session_state["chat_history"].append({"role": "image", "content": image})
                display_chat_history()

        with col4:
            if st.form_submit_button("清空"):
                st.session_state["chat_history"] = []
                # 更新对话记录容器
                chat_history_container.empty()
if get_current_page() == "settings":
    st.title("设置")
    st.markdown("在这里可以设置你的设置。")
    st.markdown("当前系统提示词（system_prompt）:" + st.session_state["system_prompt"])
    # 设置系统提示词system_prompt
    system_prompt = st.text_area("系统提示词", height=100, placeholder="请输入你的系统提示词")
    path1 = st.session_state["wf_path"]
    _path = st.selectbox(
        "选择一个包含start_workflow & end_workflow的工作流文件",
        [f for f in os.listdir(os.path.join(current_dir_path, "workflow_api")) if f.endswith(".json")],
    )
    # 保存按钮
    if st.button("保存"):
        # 保存_path到session_state
        st.session_state["wf_path"] = _path
        print(st.session_state["wf_path"])
        # 保存system_prompt到session_state
        st.session_state["system_prompt"] = system_prompt
        st.success("保存成功！")
