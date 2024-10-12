import csv
import json
import os
from collections import deque

import pandas as pd

from ..config import current_dir_path

file_path = os.path.join(current_dir_path, "KG")

KG_path = ""


class KG_csv_toolkit_developer:
    @classmethod
    def INPUT_TYPES(s):
        # 获取file_path文件夹下的所有json文件的文件名
        paths = [f for f in os.listdir(file_path) if f.endswith(".csv")]
        return {
            "required": {
                "absolute_path": ("STRING", {"default": ""}),
                "relative_path": (paths, {"default": "test.csv"}),
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
                    "name": "Inquire_triple",
                    "description": "用于查询包含实体A-关系-实体B的三元组信息，Inquire_entities会返回符合条件的所有三元组，也包括实体B-关系-实体A的三元组，请根据三元组顺序进行关系分析，如果关系被缺省，会返回实体A和实体B的所有关系，如果没有直接关系，会返回间接关系",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entitie_A": {
                                "type": "string",
                                "description": "实体A",
                            },
                            "relationship": {
                                "type": "string",
                                "description": "关系",
                            },
                            "entitie_B": {
                                "type": "string",
                                "description": "实体B",
                            },
                        },
                        "required": ["entitie_A"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "New_triple",
                    "description": "用于新增一个不存在的三元组，请在新增三元组前使用Inquire_triple工具判断三元组是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entitie_A": {
                                "type": "string",
                                "description": "实体A",
                            },
                            "relationship": {
                                "type": "string",
                                "description": "关系",
                            },
                            "entitie_B": {
                                "type": "string",
                                "description": "实体B",
                            },
                        },
                        "required": ["entitie_A", "relationship", "entitie_B"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Delete_triple",
                    "description": "用于删除一个存在的三元组，请在删除三元组前使用Inquire_entities工具判断三元组是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entitie_A": {
                                "type": "string",
                                "description": "实体A",
                            },
                            "relationship": {
                                "type": "string",
                                "description": "关系",
                            },
                            "entitie_B": {
                                "type": "string",
                                "description": "实体B",
                            },
                        },
                        "required": ["entitie_A", "relationship", "entitie_B"],
                    },
                },
            },
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class KG_csv_toolkit_user:
    @classmethod
    def INPUT_TYPES(s):
        # 获取file_path文件夹下的所有json文件的文件名
        paths = [f for f in os.listdir(file_path) if f.endswith(".csv")]
        return {
            "required": {
                "absolute_path": ("STRING", {"default": ""}),
                "relative_path": (paths, {"default": "test.csv"}),
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
                    "name": "Inquire_triple",
                    "description": "用于查询包含实体A-关系-实体B的三元组信息，Inquire_entities会返回符合条件的所有三元组，也包括实体B-关系-实体A的三元组，请根据三元组顺序进行关系分析，如果关系被缺省，会返回实体A和实体B的所有关系，如果没有直接关系，会返回间接关系",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "entitie_A": {
                                "type": "string",
                                "description": "实体A",
                            },
                            "relationship": {
                                "type": "string",
                                "description": "关系",
                            },
                            "entitie_B": {
                                "type": "string",
                                "description": "实体B",
                            },
                        },
                        "required": ["entitie_A"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


def generate_graph(entitie_A=None, relationship=None, entitie_B=None):
    with open(KG_path, "r", encoding="utf8") as fin:
        reader = csv.reader(fin)
        for row in reader:
            if entitie_A and row[0] != entitie_A:
                continue
            if relationship and row[1] != relationship:
                continue
            if entitie_B and row[2] != entitie_B:
                continue
            yield row


def Inquire_triple(entitie_A, relationship=None, entitie_B=None):
    """
    用于查询一个存在的三元组，返回三元组信息
    :param entitie_A: 实体A
    :param relationship: 关系
    :param entitie_B: 实体B
    :return: 返回三元组信息
    """
    graph = {}
    for s, p, o in generate_graph(entitie_A, relationship, entitie_B):
        if s not in graph:
            graph[s] = []
        if o not in graph:
            graph[o] = []
        graph[s].append((p, o))
        graph[o].append((p, s))

    out_list = []
    if relationship is None and entitie_B is None:
        out_list.extend(graph.get(entitie_A, []))
    elif relationship is not None and entitie_B is None:
        out_list.extend([(rel, ent) for rel, ent in graph.get(entitie_A, []) if rel == relationship])
    elif relationship is None and entitie_B is not None:
        if entitie_B in graph.get(entitie_A, []):
            out_list.extend([(rel, entitie_B) for rel, ent in graph.get(entitie_A, []) if ent == entitie_B])
        else:
            paths = find_paths_BFS(graph, entitie_A, entitie_B)
            for path in paths:
                out_list.append(path)
    else:
        if entitie_B in graph.get(entitie_A, []) and (relationship, entitie_B) in graph.get(entitie_A, []):
            out_list.append((relationship, entitie_B))

    if out_list:
        out_list = [list(t) for t in out_list]
        out = json.dumps(out_list, ensure_ascii=False, indent=4)
        return str(out)
    else:
        return "查询不到任何相关的三元组"


def find_paths_BFS(graph, start, goal):
    """
    使用广度优先搜索找到所有从start到goal的路径
    :param graph: 知识图谱的图表示
    :param start: 起始实体
    :param goal: 目标实体
    :return: 所有可能的路径列表
    """
    queue = deque([[start]])
    paths = []
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            paths.append(path)
            continue
        for _, neighbour in graph.get(node, []):
            new_path = list(path)
            new_path.append(neighbour)
            queue.append(new_path)
    return paths


def New_triple(entitie_A, relationship, entitie_B):
    """
    用于添加一个不存在的三元组，返回添加后的知识图谱
    :param entitie_A: 实体A
    :param relationship: 关系
    :param entitie_B: 实体B
    :return: 返回添加是否成功
    """
    with open(KG_path, "a", encoding="utf8") as fin:
        writer = csv.writer(fin)
        writer.writerow([entitie_A, relationship, entitie_B])
        return "添加成功"


def Delete_triple(entitie_A, relationship, entitie_B):
    """
    用于删除一个存在的三元组，返回删除后的知识图谱
    :param entitie_A: 实体A
    :param relationship: 关系
    :param entitie_B: 实体B
    :param chunk_size: 每次读取的行数
    :return: 返回删除是否成功
    """
    temp_path = KG_path + ".tmp"
    with open(KG_path, "r", encoding="utf8") as fin, open(temp_path, "w", encoding="utf8", newline="") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            if row[0] != entitie_A or row[1] != relationship or row[2] != entitie_B:
                writer.writerow(row)

    # 替换原文件
    os.replace(temp_path, KG_path)
    return "删除成功"
