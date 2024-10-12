import json

from neo4j import GraphDatabase

database_url_hold = "bolt://localhost:7687"
database_name_hold = "neo4j"
password_hold = "12345678"


class KG_neo_toolkit_developer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "database_url": ("STRING", {"default": "bolt://localhost:7687"}),
                "database_name": ("STRING", {"default": "neo4j"}),
                "password": ("STRING", {"default": "12345678"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, database_url, database_name, password, is_enable=True):
        if is_enable == False:
            return (None,)
        global database_url_hold, database_name_hold, password_hold
        database_url_hold = database_url
        database_name_hold = database_name
        password_hold = password
        output = [
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entities_neo4j",
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
                    "name": "New_entities_neo4j",
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
                    "name": "Modify_entities_neo4j",
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
                    "name": "Delete_entities_neo4j",
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
                    "name": "Inquire_relationships_neo4j",
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
                    "name": "New_relationships_neo4j",
                    "description": "用于新增一个不存在的关系边， 请在新增关系边前使用Inquire_relationships工具判断关系边是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "关系的label，例如：'朋友'",
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
                        "required": ["label", "source", "target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Modify_relationships_neo4j",
                    "description": "用于修改一个存在的关系边， 请在修改关系边前使用Inquire_relationships工具判断关系边是否存在，你输入的attributes会覆盖已有的attributes，所以输入的attributes必须包含之前查询到的attributes信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "关系的label，例如：'朋友'",
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
                        "required": ["label", "source", "target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Delete_relationships_neo4j",
                    "description": "用于删除一个存在的关系边，请在删除关系边前使用Inquire_relationships工具判断关系边是否存在",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "关系的label，例如：'朋友'",
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
                        "required": ["label", "source", "target"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entity_relationships_neo4j",
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
                    "name": "Inquire_entity_list_neo4j",
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


class KG_neo_toolkit_user:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "database_name": ("STRING", {"default": "neo4j"}),
                "password": ("STRING", {"default": "12345678"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tools",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, database_name, password, is_enable=True):
        if is_enable == False:
            return (None,)
        global database_name_hold, password_hold
        database_name_hold = database_name
        password_hold = password
        output = [
            {
                "type": "function",
                "function": {
                    "name": "Inquire_entities_neo4j",
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
                    "name": "Inquire_relationships_neo4j",
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
                    "name": "Inquire_entity_relationships_neo4j",
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
                    "name": "Inquire_entity_list_neo4j",
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


def Inquire_entities_neo4j(name):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    with driver.session() as session:
        result = session.run("MATCH (n {name: $name}) RETURN n", name=name)
        entities = [record["n"] for record in result]
    driver.close()
    if not entities:
        return "该实体节点不存在"
    return str(entities)


def New_entities_neo4j(name, attributes=None):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    if attributes is None:
        attributes = {}
    else:
        attributes = json.loads(attributes)

    with driver.session() as session:
        result = session.run("MATCH (n {name: $name}) RETURN n", name=name)
        if result.single():
            return "该实体节点已存在"

        # Create the query string with dynamic attributes
        attr_str = ", ".join([f"{key}: ${key}" for key in attributes.keys()])
        if attr_str:
            query = f"CREATE (n:{name.replace(' ', '_')} {{name: $name, {attr_str}}})"
        else:
            query = f"CREATE (n:{name.replace(' ', '_')} {{name: $name}})"

        # Run the query with the attributes
        session.run(query, name=name, **attributes)

    driver.close()
    return "添加成功"


def Modify_entities_neo4j(name, attributes=None):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))

    if attributes is None:
        attributes = {}
    else:
        attributes = json.loads(attributes)

    with driver.session() as session:
        # 创建包含动态属性的查询字符串
        set_attr_str = ", ".join([f"n.{key} = ${key}" for key in attributes.keys()])

        # 查询所有属性并删除未包含在 attributes 中的属性
        query = (
            f"MATCH (n:{name.replace(' ', '_')} {{name: $name}}) SET {set_attr_str} "
            + " ".join([f"REMOVE n.{key}" for key in attributes.keys() if key not in attributes])
            + ""
        )  # 添加闭合的引号

        # 运行查询
        result = session.run(query, name=name, **attributes)
        if not result.single():
            return "该实体节点不存在"

    driver.close()
    return "修改成功"


def Delete_entities_neo4j(name):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    with driver.session() as session:
        query = f"MATCH (n:{name.replace(' ', '_')} {{name: $name}}) DETACH DELETE n RETURN n"
        result = session.run(query, name=name)
        if not result.single():
            return "该实体节点不存在"
    driver.close()
    return "删除成功"


def Inquire_relationships_neo4j(entitie_A, entitie_B):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    with driver.session() as session:
        # Check if entities exist
        result = session.run(
            """
            MATCH (a {name: $entitie_A})
            RETURN a
            """,
            entitie_A=entitie_A,
        )
        if not result.single():
            return f"实体 {entitie_A} 不存在"

        result = session.run(
            """
            MATCH (b {name: $entitie_B})
            RETURN b
            """,
            entitie_B=entitie_B,
        )
        if not result.single():
            return f"实体 {entitie_B} 不存在"

        # Check direct relationships
        result = session.run(
            """
            MATCH (a {name: $entitie_A})-[r]->(b {name: $entitie_B})
            RETURN r
            """,
            entitie_A=entitie_A,
            entitie_B=entitie_B,
        )
        relationships = [record["r"] for record in result]
        if relationships:
            return "两者之间的直接关系为：" + str(relationships)

        result = session.run(
            """
            MATCH (b {name: $entitie_B})-[r]->(a {name: $entitie_A})
            RETURN r
            """,
            entitie_A=entitie_A,
            entitie_B=entitie_B,
        )
        reverse_relationships = [record["r"] for record in result]
        if reverse_relationships:
            return "两者之间的反向直接关系为：" + str(reverse_relationships)

        # Check shortest path
        result = session.run(
            """
            MATCH path = shortestPath((a {name: $entitie_A})-[*]-(b {name: $entitie_B}))
            RETURN path
            """,
            entitie_A=entitie_A,
            entitie_B=entitie_B,
        )
        shortest_path = [record["path"] for record in result]
        if shortest_path:
            path_details = []
            for path in shortest_path:
                nodes = [node["name"] for node in path.nodes]
                relationships = []
                for rel in path.relationships:
                    start_node = rel.start_node["name"]
                    end_node = rel.end_node["name"]
                    rel_type = rel.type
                    relationships.append(f"{start_node}-[{rel_type}]->{end_node}")
                path_details.append({"nodes": nodes, "relationships": relationships})
            return "两者之间不存在直接关系，最短关系链为：" + str(path_details)

    driver.close()
    return "两者之间不存在任何直接或间接关系"


def New_relationships_neo4j(source, target, label, attributes=None):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    if attributes is None:
        attributes = {}
    else:
        attributes = json.loads(attributes)

    with driver.session() as session:
        # Check if entities exist
        result = session.run(
            """
            MATCH (a {name: $source})
            RETURN a
            """,
            source=source,
        )
        if not result.single():
            return f"实体 {source} 不存在"

        result = session.run(
            """
            MATCH (b {name: $target})
            RETURN b
            """,
            target=target,
        )
        if not result.single():
            return f"实体 {target} 不存在"

        # Check if relationship already exists
        result = session.run(
            """
            MATCH (a {name: $source})-[r:`"""
            + label.replace(" ", "_")
            + """`]->(b {name: $target})
            RETURN r
            """,
            source=source,
            target=target,
        )
        if result.single():
            return "该关系边已存在"

        # Create the query string with dynamic attributes
        attr_str = ", ".join([f"{key}: ${key}" for key in attributes.keys()])
        if attr_str:
            query = f"""
                MATCH (a {{name: $source}}), (b {{name: $target}})
                CREATE (a)-[r:`{label.replace(' ', '_')}` {{ {attr_str} }}]->(b)
            """
        else:
            query = f"""
                MATCH (a {{name: $source}}), (b {{name: $target}})
                CREATE (a)-[r:`{label.replace(' ', '_')}`]->(b)
            """

        # Run the query with the attributes
        session.run(query, source=source, target=target, **attributes)

    driver.close()
    return "添加成功"


def Modify_relationships_neo4j(source, target, label, attributes=None):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    if attributes is None:
        attributes = {}
    else:
        attributes = json.loads(attributes)

    with driver.session() as session:
        # Check if entities exist
        result = session.run(
            """
            MATCH (a {name: $source})
            RETURN a
            """,
            source=source,
        )
        if not result.single():
            return f"实体 {source} 不存在"

        result = session.run(
            """
            MATCH (b {name: $target})
            RETURN b
            """,
            target=target,
        )
        if not result.single():
            return f"实体 {target} 不存在"

        # Create the query string with dynamic attributes
        attr_str = ", ".join([f"r.{key} = ${key}" for key in attributes.keys()])
        if attr_str:
            query = f"""
                MATCH (a {{name: $source}})-[r:`{label.replace(' ', '_')}`]->(b {{name: $target}})
                SET {attr_str}
                RETURN r
            """
        else:
            query = f"""
                MATCH (a {{name: $source}})-[r:`{label.replace(' ', '_')}`]->(b {{name: $target}})
                RETURN r
            """

        # Run the query with the attributes
        result = session.run(query, source=source, target=target, **attributes)
        if not result.single():
            return "该关系边不存在"

    driver.close()
    return "修改成功"


def Delete_relationships_neo4j(source, target, label):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a {name: $source})-[r:`"""
            + label.replace(" ", "_")
            + """` {name: $label}]->(b {name: $target})
            DELETE r
            RETURN r
        """,
            source=source,
            target=target,
            label=label,
        )
        if not result.single():
            return "该关系边不存在"
    driver.close()
    return "删除成功"


def Inquire_entity_relationships_neo4j(name):
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    with driver.session() as session:
        result = session.run("MATCH (n {name: $name}) RETURN n", name=name)
        if not result.single():
            return "实体" + name + "不存在"
        result = session.run(
            """
            MATCH (n {name: $name})-[r]-(m)
            RETURN r
        """,
            name=name,
        )
        relationships = [record["r"] for record in result]
    driver.close()
    return "实体" + name + "的关系边为：" + str(relationships)


def Inquire_entity_list_neo4j():
    global database_url_hold, database_name_hold, password_hold
    driver = GraphDatabase.driver(database_url_hold, auth=(database_name_hold, password_hold))
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n.name")
        name_list = [record["n.name"] for record in result]
    driver.close()
    return "实体列表为：" + str(name_list)
