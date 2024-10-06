import base64
import configparser
import json
import locale
import os
import time

import requests
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
output_path = os.path.join(current_dir, "output")


driver = None
img_api_key = None
element = None
service = None


def is_browser_closed(driver):
    try:
        # 尝试访问一个属性或方法
        driver.title
        return False
    except WebDriverException:
        return True


def driver_init():
    global driver, service

    # 判断当前浏览器是否已经打开
    if driver is not None and not is_browser_closed(driver):
        return "浏览器已经初始化"

    # 如果浏览器未打开或已关闭，重新初始化
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()  # 设置浏览器窗口最大化
    return "初始化成功"


def driver_get(url):
    global driver
    driver.get(url)
    return "成功打开"


def driver_back():
    global driver
    driver.back()
    return "返回上一页"


def driver_forward():
    global driver
    driver.forward()
    return "前进到下一页"


def driver_refresh():
    global driver
    driver.refresh()
    return "刷新当前页面"


def driver_close():
    global driver
    driver.close()
    return "关闭当前窗口"


def driver_quit():
    global driver
    driver.quit()
    return "关闭所有窗口并退出 WebDriver"


def switch_to_window(window_name):
    global driver
    driver.switch_to.window(window_name)
    return f"切换到窗口: {window_name}"


def get_current_window_handle():
    global driver
    return str(driver.current_window_handle)


def get_window_handles():
    global driver
    return json.dumps(driver.window_handles)


def get_current_url():
    global driver
    return str(driver.current_url)


def get_title():
    global driver
    return str(driver.title)


def tag_name_search(tag_name, search_term=None, text_length_limit=100):
    global driver
    elements = driver.find_elements(By.TAG_NAME, tag_name)
    elements_dict = {}

    for index, element in enumerate(elements):
        element_id = element.get_attribute("id")
        element_type = element.get_attribute("type")
        element_name = element.get_attribute("name")
        element_placeholder = element.get_attribute("placeholder")
        element_title = element.get_attribute("title")
        element_aria_label = element.get_attribute("aria-label")
        element_alt = element.get_attribute("alt")
        element_text = element.text

        if tag_name in ["img", "video", "audio", "iframe", "source"]:
            element_url = element.get_attribute("src")
        elif tag_name in ["a", "link"]:
            element_url = element.get_attribute("href")
        else:
            element_url = None

        element_info = {
            "id": element_id,
            "url": element_url,
            "text": element_text,
            "type": element_type,
            "name": element_name,
            "placeholder": element_placeholder,
            "title": element_title,
            "aria-label": element_aria_label,
            "alt": element_alt,
        }

        # 移除空属性
        element_info = {k: v for k, v in element_info.items() if v}

        if search_term:
            if any(search_term in (value or "") for value in element_info.values()):
                elements_dict[f"{tag_name}_{index}"] = element_info
        else:
            # 如果element_info有text属性，则截取前text_length_limit个字符
            if "text" in element_info:
                element_info["text"] = element_info["text"][:text_length_limit]
            elements_dict[f"{tag_name}_{index}"] = element_info

    # 返回字典的json字符串
    res = json.dumps(elements_dict, ensure_ascii=False)
    print(res)
    return res


def select_and_interact_with_element(tag_name, Attribute_dict, interact, input_text=None):
    global driver, element
    try:
        # 解析 JSON 字符串为字典
        attribute_dict = json.loads(Attribute_dict)

        # 获取所有指定标签名的元素
        elements = driver.find_elements(By.TAG_NAME, tag_name)

        for elem in elements:
            match = True
            for key, value in attribute_dict.items():
                if key == "text":
                    if value != elem.text:
                        match = False
                else:
                    if elem.get_attribute(key) != value:
                        match = False

            if match:
                element = elem
                break
            else:
                element = None
        if element is None:
            return "未找到匹配的元素"
        if interact == "click":
            try:
                element.click()
                return "点击成功"
            except:
                return "点击失败"
        elif interact == "send_submit":
            try:
                element.send_keys(input_text)
                time.sleep(0.5)
                element.submit()
                return "输入并提交成功"
            except:
                return "输入或提交失败"
        elif interact == "get_text":
            try:
                return element.text
            except:
                return "获取文本失败"
        elif interact == "clear":
            try:
                element.clear()
                return "清除成功"
            except:
                return "清除失败"
        else:
            return "未知的交互方式"
    except json.JSONDecodeError:
        return "JSON 解析错误"


def driver_save_screenshot():
    global driver, output_path, img_api_key
    # 时间戳
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 截图文件名
    screenshot_file = f"screenshot_{timestamp}.png"
    # output_path截图
    screenshot_path = os.path.join(output_path, screenshot_file)
    driver.save_screenshot(screenshot_path)
    # 上传到imgbb
    with open(screenshot_path, "rb") as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": img_api_key, "image": image_base64}
    # 向API发送POST请求
    response = requests.post(url, data=payload)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析响应以获取图片URL
        result = response.json()
        img_url = result["data"]["url"]
    else:
        return "Error: " + response.text
    return [
        {"type": "text", "text": "当前浏览器截图已保存，请查看"},
        {
            "type": "image_url",
            "image_url": {
                "url": img_url,
            },
        },
    ]


class selenium_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "driver_path": (
                    "STRING",
                    {"default": "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"},
                ),
                "imgbb_api_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "selenium_driver"

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def selenium_driver(self, driver_path, imgbb_api_key, is_enable=True):

        if not is_enable:
            return (None,)
        global img_api_key, service
        service = Service(driver_path)
        img_api_key = imgbb_api_key
        output = [
            {
                "type": "function",
                "function": {
                    "name": "driver_init",
                    "description": "使用selenium库的driver初始化浏览器，如果已经初始化过，则不会有任何影响，在开始调用其他方法前，请先调用此方法。如果你关闭了浏览器，需要重新调用此方法",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_get",
                    "description": "使用selenium库的driver打开指定网页",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "需要打开的网页地址",
                            }
                        },
                        "required": ["url"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_save_screenshot",
                    "description": "使用selenium库的driver截图，并返回截图的URL，当你想要查看当前页面的画面时可以调用这个方法，你可以查看截图的URL以判断执行效果和当前浏览器状态",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_back",
                    "description": "使用selenium库的driver返回上一页",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_forward",
                    "description": "使用selenium库的driver前进到下一页",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_refresh",
                    "description": "使用selenium库的driver刷新当前页面",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_close",
                    "description": "使用selenium库的driver关闭当前窗口",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "driver_quit",
                    "description": "使用selenium库的driver关闭所有窗口并退出 WebDriver",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "switch_to_window",
                    "description": "使用selenium库的driver切换到指定窗口",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "window_name": {
                                "type": "string",
                                "description": "需要切换的窗口名称",
                            }
                        },
                        "required": ["window_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_window_handle",
                    "description": "使用selenium库的driver获取当前窗口句柄",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_window_handles",
                    "description": "使用selenium库的driver获取所有窗口句柄",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_url",
                    "description": "使用selenium库的driver获取当前页面的 URL",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_title",
                    "description": "使用selenium库的driver获取当前页面的标题",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tag_name_search",
                    "description": "使用selenium库的driver获取当前页面同一tag name的所有与search_term相关的元素，会返回包含这些元素的元素id和信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tag_name": {
                                "type": "string",
                                "description": "要搜索的tag name(HTML 标签),例如但不限于：'a','image','video','audio','button'",
                            },
                            "search_term": {
                                "type": "string",
                                "description": "要搜索的文本信息，如果不填，则返回所有该tag name的元素",
                            },
                        },
                    },
                    "required": ["tag_name"],
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "select_and_interact_with_element",
                    "description": "使用selenium库的driver的find_element锁定当前页面符合条件的元素，然后进行操作。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tag_name": {
                                "type": "string",
                                "description": "要搜索的tag name(HTML 标签),例如但不限于：'a','image','video','audio','button'",
                            },
                            "Attribute_dict": {
                                "type": "string",
                                "description": '要搜索的属性的json字典，例如：{"type": "text", "name": "search"}',
                            },
                            "interact": {
                                "type": "string",
                                "description": "要进行的操作，可选项：'click','send_submit','clear','get_text'。",
                            },
                            "input_text": {
                                "type": "string",
                                "description": "如果interact为'send_submit'，则此参数为要输入的文本。",
                            },
                        },
                    },
                    "required": ["tag_name", "Attribute_dict", "interact"],
                },
            },
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


_TOOL_HOOKS = [
    "driver_init",
    "driver_get",
    "driver_save_screenshot",
    "driver_back",
    "driver_forward",
    "driver_refresh",
    "driver_close",
    "driver_quit",
    "switch_to_window",
    "get_current_window_handle",
    "get_window_handles",
    "get_current_url",
    "get_title",
    "tag_name_search",
    "select_and_interact_with_element",
]
NODE_CLASS_MAPPINGS = {
    "selenium_tool": selenium_tool,
}
lang = locale.getdefaultlocale()[0]
import configparser

config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language == "en_US":
    lang = language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"selenium_tool": "浏览器自动控制工具包"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"selenium_tool": "Browser Auto Control Toolkit"}
