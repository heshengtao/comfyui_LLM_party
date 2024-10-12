import json

import requests


class api_box:
    def __init__(self, id, url, api_key="") -> None:
        self.id = id
        self.url = url
        self.api_key = api_key

    def request_api(self, **parameter):

        if self.api_key != None and self.api_key != "":
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(self.url, params=parameter, headers=headers, timeout=10)
        else:
            response = requests.get(self.url, params=parameter, timeout=10)

        if response.status_code == 200:
            # 解析 JSON 响应并自动处理 Unicode 转义字符
            json_data = json.loads(response.content.decode("utf-8"))
            # 将 JSON 数据转换回字符串
            out = json.dumps(json_data, ensure_ascii=False, indent=4)
        else:
            out = "API请求失败"

        return out


api_boxes = {}


def use_api_tool(id, **parameter):
    global api_boxes
    if str(id).strip() in api_boxes:
        return api_boxes[str(id).strip()].request_api(**parameter)
    else:
        return "API ID不存在"


class api_tool:
    def __init__(self) -> None:
        # 哈希值给到ID
        self.id = hash(self)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "url": ("STRING", {"default": "被请求的网址"}),
                "api_key": ("STRING", {"default": ""}),
                "description": ("STRING", {"multiline": True, "default": "用来查天气的工具"}),
                "parameters": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": """
{
    "city": "用户询问的目标区域，例如：长沙市",
    "extensions": "可选值：base/all base:返回实况天气 all:返回预报天气，默认为all"
}
""",
                    },
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "read_web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/自动化（Automation）"

    def read_web(self, url, description, parameters, api_key="", is_enable=True):
        if is_enable == False:
            return (None,)
        global api_boxes
        api_boxes[str(self.id).strip()] = api_box(self.id, url, api_key)

        if parameters:
            try:
                parameters = json.loads(parameters)
            except:
                return ("参数格式错误，请检查",)
        parameter = {"id": {"type": "string", "description": "API ID=" + str(self.id).strip()}}
        required = ["id"]
        for key in parameters:
            parameter[key] = {"type": "string", "description": parameters[key]}
            required.append(key)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "use_api_tool",
                    "description": description,
                    "parameters": {"type": "object", "properties": parameter, "required": required},
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class api_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"default": "被请求的网址"}),
                "api_key": ("STRING", {"default": ""}),
                "parameters": (
                    "DICT",
                    {"forceInput": True},
                ),
            },
            "optional": {
                "request_type": (["get", "post"], {"default": "get"}),
                "timeout": ("INT", {"default": 60}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "api"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def api(self, url, parameters, api_key="", request_type="get", timeout=60):
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

        if request_type.lower() == "post":
            response = requests.post(url, json=parameters, headers=headers, timeout=timeout)
        else:  # 默认使用 GET 请求
            response = requests.get(url, params=parameters, headers=headers, timeout=timeout)

        if response.status_code == 200:
            # 解析 JSON 响应并自动处理 Unicode 转义字符
            json_data = json.loads(response.content.decode("utf-8"))
            # 将 JSON 数据转换回字符串
            out = json.dumps(json_data, ensure_ascii=False, indent=4)
        else:
            out = "API请求失败"

        return (out,)


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


class parameter_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": ""}),
                "value": (any_type, {}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("parameter",)

    FUNCTION = "parameter"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def parameter(self, key="", value=""):
        out = {key: value}
        return (out,)


class parameter_combine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "parameter1": ("DICT", {"forceInput": True}),
                "parameter2": ("DICT", {"forceInput": True}),
                "parameter3": ("DICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("parameters",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(self, parameter1=None, parameter2=None, parameter3=None):
        parameter = {}
        if parameter1 is not None:
            for key, value in parameter1.items():
                parameter[key] = value
        if parameter2 is not None:
            for key, value in parameter2.items():
                parameter[key] = value
        if parameter3 is not None:
            for key, value in parameter3.items():
                parameter[key] = value
        return (parameter,)


class parameter_combine_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "parameter1": ("DICT", {"forceInput": True}),
                "parameter2": ("DICT", {"forceInput": True}),
                "parameter3": ("DICT", {"forceInput": True}),
                "parameter4": ("DICT", {"forceInput": True}),
                "parameter5": ("DICT", {"forceInput": True}),
                "parameter6": ("DICT", {"forceInput": True}),
                "parameter7": ("DICT", {"forceInput": True}),
                "parameter8": ("DICT", {"forceInput": True}),
                "parameter9": ("DICT", {"forceInput": True}),
                "parameter10": ("DICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("parameters",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(
        self,
        parameter1=None,
        parameter2=None,
        parameter3=None,
        parameter4=None,
        parameter5=None,
        parameter6=None,
        parameter7=None,
        parameter8=None,
        parameter9=None,
        parameter10=None,
    ):

        parameter = {}

        if parameter1 is not None:
            for key, value in parameter1.items():
                parameter[key] = value
        if parameter2 is not None:
            for key, value in parameter2.items():
                parameter[key] = value
        if parameter3 is not None:
            for key, value in parameter3.items():
                parameter[key] = value
        if parameter4 is not None:
            for key, value in parameter4.items():
                parameter[key] = value
        if parameter5 is not None:
            for key, value in parameter5.items():
                parameter[key] = value
        if parameter6 is not None:
            for key, value in parameter6.items():
                parameter[key] = value
        if parameter7 is not None:
            for key, value in parameter7.items():
                parameter[key] = value
        if parameter8 is not None:
            for key, value in parameter8.items():
                parameter[key] = value
        if parameter9 is not None:
            for key, value in parameter9.items():
                parameter[key] = value
        if parameter10 is not None:
            for key, value in parameter10.items():
                parameter[key] = value

        return (parameter,)


class list_append:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "any1": (any_type, {}),
                "any2": (any_type, {}),
                "any3": (any_type, {}),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(self, any1=None, any2=None, any3=None):
        lists = []
        if any1 is not None:
            lists.append(any1)
        if any2 is not None:
            lists.append(any2)
        if any3 is not None:
            lists.append(any3)

        return (lists,)


class list_append_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "any1": (any_type, {}),
                "any2": (any_type, {}),
                "any3": (any_type, {}),
                "any4": (any_type, {}),
                "any5": (any_type, {}),
                "any6": (any_type, {}),
                "any7": (any_type, {}),
                "any8": (any_type, {}),
                "any9": (any_type, {}),
                "any10": (any_type, {}),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(
        self,
        any1=None,
        any2=None,
        any3=None,
        any4=None,
        any5=None,
        any6=None,
        any7=None,
        any8=None,
        any9=None,
        any10=None,
    ):
        lists = []
        if any1 is not None:
            lists.append(any1)
        if any2 is not None:
            lists.append(any2)
        if any3 is not None:
            lists.append(any3)
        if any4 is not None:
            lists.append(any4)
        if any5 is not None:
            lists.append(any5)
        if any6 is not None:
            lists.append(any6)
        if any7 is not None:
            lists.append(any7)
        if any8 is not None:
            lists.append(any8)
        if any9 is not None:
            lists.append(any9)
        if any10 is not None:
            lists.append(any10)
        return (lists,)


class list_extend:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "list1": ("LIST", {}),
                "list2": ("LIST", {}),
                "list3": ("LIST", {}),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(self, list1=None, list2=None, list3=None):
        lists = []
        if list1 is not None:
            lists.extend(list1)
        if list2 is not None:
            lists.extend(list2)
        if list3 is not None:
            lists.extend(list3)

        return (lists,)


class list_extend_plus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "list1": ("LIST", {}),
                "list2": ("LIST", {}),
                "list3": ("LIST", {}),
                "list4": ("LIST", {}),
                "list5": ("LIST", {}),
                "list6": ("LIST", {}),
                "list7": ("LIST", {}),
                "list8": ("LIST", {}),
                "list9": ("LIST", {}),
                "list10": ("LIST", {}),
            },
        }

    RETURN_TYPES = ("LISTS",)
    RETURN_NAMES = ("lists",)

    FUNCTION = "combine"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/组合（combine）"

    def combine(
        self,
        list1=None,
        list2=None,
        list3=None,
        list4=None,
        list5=None,
        list6=None,
        list7=None,
        list8=None,
        list9=None,
        list10=None,
    ):
        lists = []
        if list1 is not None:
            lists.extend(list1)
        if list2 is not None:
            lists.extend(list2)
        if list3 is not None:
            lists.extend(list3)
        if list4 is not None:
            lists.extend(list4)
        if list5 is not None:
            lists.extend(list5)
        if list6 is not None:
            lists.extend(list6)
        if list7 is not None:
            lists.extend(list7)
        if list8 is not None:
            lists.extend(list8)
        if list9 is not None:
            lists.extend(list9)
        if list10 is not None:
            lists.extend(list10)

        return (lists,)


class json2text:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "JSON": (any_type, {}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "parameter"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def parameter(self, JSON=""):
        # 把 json 转换成 text
        out = json.dumps(JSON, ensure_ascii=False, indent=4)
        return (out,)
