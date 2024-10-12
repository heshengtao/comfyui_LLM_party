import json
import os
from collections import deque

from ..config import current_dir_path

file_path = os.path.join(current_dir_path, "KG")

KG_path = ""


class KG_json_toolkit_developer:
    @classmethod
    def INPUT_TYPES(s):
        # 获取file_path文件夹下的所有json文件的文件名
        paths = [f for f in os.listdir(file_path) if f.endswith(".json")]
        return {
            "required": {
                "absolute_path": ("STRING", {"default": ""}),
                "relative_path": (paths, {"default": "test.json"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, relative_path, absolute_path="", is_enable=True):
        if is_enable == False:
            return (None,)
        global KG_path
        if absolute_path != "":
            KG_path = absolute_path
        else:
            KG_path = os.path.join(file_path, relative_path)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entities",
                    "description": "用于查询实体节点的相关信息，可以用来判断实体是否存在，以选择使用新增实体还是修改实体工具",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            }
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "New_entities",
                    "description": "用于新增一个不存在的实体节点，请在新增实体节点前使用Inquire_entities工具判断实体是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            },
                            "attributes": {
                                "type": "string",
                                "description": "实体的attributes，例如：{'name': '张三', 'age': 20}，缺省时，attributes为空",
                            },
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Modify_entities",
                    "description": "用于修改一个存在的实体节点，请在修改实体节点前使用Inquire_entities工具判断实体是否存在，你输入的attributes会覆盖已有的attributes，所以输入的attributes必须包含之前查询到的attributes信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            },
                            "attributes": {
                                "type": "string",
                                "description": "实体的attributes，例如：{'name': '张三', 'age': 20}，缺省时，会删除已有的attributes信息",
                            },
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Delete_entities",
                    "description": "用于删除一个存在的实体节点，请在删除实体节点前使用Inquire_entities工具判断实体是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            }
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_relationships",
                    "description": "用于查询关系边的相关信息，entitie_A和entitie_B的顺序可能会颠倒",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entitie_A": {
                                "type": "string",
                                "description": "关系中的其中一个节点的name",
                            },
                            "entitie_B": {
                                "type": "string",
                                "description": "关系中的其中另一个节点的name",
                            },
                        },
                        "required": ["entitie_A", "entitie_B"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "New_relationships",
                    "description": "用于新增一个不存在的关系边， 请在新增关系边前使用Inquire_relationships工具判断关系边是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "关系的type，例如：'朋友'",
                            },
                            "source": {
                                "type": "string",
                                "description": "关系的source，代表源节点的name",
                            },
                            "target": {
                                "type": "string",
                                "description": "关系的target，代表目标节点的name",
                            },
                            "attributes": {
                                "type": "object",
                                "description": "关系的属性，例如：{'起始于':'2010年'}，缺省时，attributes为空",
                            },
                        },
                        "required": ["type", "source", "target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Modify_relationships",
                    "description": "用于修改一个存在的关系边， 请在修改关系边前使用Inquire_relationships工具判断关系边是否存在，你输入的attributes会覆盖已有的attributes，所以输入的attributes必须包含之前查询到的attributes信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "关系的type，例如：'朋友'",
                            },
                            "source": {
                                "type": "string",
                                "description": "关系的source，代表源节点的name",
                            },
                            "target": {
                                "type": "string",
                                "description": "关系的target，代表目标节点的name",
                            },
                            "attributes": {
                                "type": "object",
                                "description": "关系的属性，例如：{'起始于':'2010年'}，缺省时会删除已有的attributes信息",
                            },
                        },
                        "required": ["type", "source", "target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Delete_relationships",
                    "description": "用于删除一个存在的关系边，请在删除关系边前使用Inquire_relationships工具判断关系边是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "关系的type，例如：'朋友'",
                            },
                            "source": {
                                "type": "string",
                                "description": "关系的source，代表源节点的name",
                            },
                            "target": {
                                "type": "string",
                                "description": "关系的target，代表目标节点的name",
                            },
                        },
                        "required": ["type", "source", "target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entity_relationships",
                    "description": "用于查询一个已存在的实体连接的所有关系边，请在查询关系边前使用Inquire_entities工具判断实体是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            }
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entity_list",
                    "description": "用于查询所有实体节点name",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class KG_json_toolkit_user:
    @classmethod
    def INPUT_TYPES(s):
        # 获取file_path文件夹下的所有json文件的文件名
        paths = [f for f in os.listdir(file_path) if f.endswith(".json")]
        return {
            "required": {
                "absolute_path": ("STRING", {"default": ""}),
                "relative_path": (paths, {"default": "test.json"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, relative_path, absolute_path="", is_enable=True):
        if is_enable == False:
            return (None,)
        global KG_path
        if absolute_path != "":
            KG_path = absolute_path
        else:
            KG_path = os.path.join(file_path, relative_path)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entities",
                    "description": "用于查询实体节点的相关信息，可以用来判断实体是否存在，以选择使用新增实体还是修改实体工具",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            }
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_relationships",
                    "description": "用于查询关系边的相关信息，entitie_A和entitie_B的顺序可能会颠倒",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entitie_A": {
                                "type": "string",
                                "description": "关系中的其中一个节点的name",
                            },
                            "entitie_B": {
                                "type": "string",
                                "description": "关系中的其中另一个节点的name",
                            },
                        },
                        "required": ["entitie_A", "entitie_B"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entity_relationships",
                    "description": "用于查询一个已存在的实体连接的所有关系边，请在查询关系边前使用Inquire_entities工具判断实体是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "实体的name",
                            }
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entity_list",
                    "description": "用于查询所有实体节点name",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


def Inquire_entities(name):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for i in data["entities"]:
        if i["name"] == name:
            out.append(i)
    if len(out) == 0:
        out = "该实体节点不存在"
    return str(out)


def New_entities(name, attributes=None):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 检查实体节点是否已存在
    for i in data["entities"]:
        if i["name"] == name:
            return "该实体节点已存在" + "\n" + "实体节点信息：" + "\n" + str(i)
    # 添加实体节点
    if attributes is None:
        attributes = "{}"
    data["entities"].append({"name": name, "attributes": json.loads(attributes)})
    with open(KG_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "添加成功"


def Modify_entities(name, attributes=None):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    is_exist = False
    if attributes is None:
        attributes = "{}"
    # 检查实体节点是否存在
    for i in data["entities"]:
        if i["name"] == name:
            i["attributes"] = json.loads(attributes)
            is_exist = True
    if is_exist:
        with open(KG_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return "修改成功"
    else:
        return "该实体节点不存在"


def Delete_entities(name):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    is_exist = False
    # 检查实体节点是否存在
    for i in data["entities"]:
        if i["name"] == name:
            data["entities"].remove(i)
            is_exist = True
    if is_exist:
        with open(KG_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return "删除成功"
    else:
        return "该实体节点不存在"


def build_graph(data):
    graph = {}
    for rel in data["relationships"]:
        source, target = rel["source"], rel["target"]
        if source not in graph:
            graph[source] = []
        if target not in graph:
            graph[target] = []
        graph[source].append((target, rel))
        graph[target].append((source, rel))  # 如果关系是双向的
    return graph


def bfs_shortest_path(graph, start, target):
    visited = set()
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        if current == target:
            return path
        visited.add(current)
        for neighbor, relationship in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [relationship]))
    return []


def Inquire_relationships(entitie_A, entitie_B):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 直接关系查询
    direct_relationships = [
        rel for rel in data["relationships"] if rel["source"] == entitie_A and rel["target"] == entitie_B
    ]
    if direct_relationships:
        return "两者之间的直接关系为：" + json.dumps(direct_relationships, ensure_ascii=False, indent=4)
    # 反向查询
    reverse_relationships = [
        rel for rel in data["relationships"] if rel["source"] == entitie_B and rel["target"] == entitie_A
    ]
    if reverse_relationships:
        return "两者之间的反向直接关系为：" + json.dumps(reverse_relationships, ensure_ascii=False, indent=4)

    # 构建图并查询最短关系链
    graph = build_graph(data)
    shortest_path = bfs_shortest_path(graph, entitie_A, entitie_B)
    if shortest_path:
        return "两者之间不存在直接关系，最短关系链为：" + json.dumps(shortest_path, ensure_ascii=False, indent=4)

    return "两者之间不存在任何直接或间接关系"


def New_relationships(source, target, type, attributes=None):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 检查关系边是否已存在
    for i in data["relationships"]:
        if i["source"] == source and i["target"] == target:
            if i["type"] == type:
                return "该关系边已存在" + "\n" + "关系边信息：" + "\n" + str(i)
    # 添加关系边
    if attributes is None:
        attributes = "{}"
    data["relationships"].append(
        {"type": type, "source": source, "target": target, "attributes": json.loads(attributes)}
    )
    with open(KG_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "添加成功"


def Modify_relationships(source, target, type, attributes=None):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    is_exist = False
    if attributes is None:
        attributes = "{}"
    # 检查关系边是否存在
    for i in data["relationships"]:
        if i["source"] == source and i["target"] == target:
            if i["type"] == type:
                i["attributes"] = json.loads(attributes)
                is_exist = True
    if is_exist:
        with open(KG_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            return "修改成功"
    else:
        return "该关系边不存在"


def Delete_relationships(source, target, type):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 检查关系边是否存在
    for i in data["relationships"]:
        if i["source"] == source and i["target"] == target:
            if i["type"] == type:
                data["relationships"].remove(i)
                with open(KG_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    return "删除成功"
    return "该关系边不存在"


def Inquire_entity_relationships(name):
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    is_exist = False
    # 检查实体是否存在
    for i in data["entities"]:
        if i["name"] == name:
            is_exist = True
            break
    if is_exist:
        # 查询实体关系
        relationships = [i for i in data["relationships"] if i["source"] == name or i["target"] == name]
        return "实体" + name + "的关系边为：" + "\n" + str(relationships)
    else:
        return "实体" + name + "不存在"


def Inquire_entity_list():
    with open(KG_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    name_list = []
    # 返回所有实体的name
    for i in data["entities"]:
        name_list.append(i["name"])
    return "实体列表为：" + "\n" + str(name_list)
