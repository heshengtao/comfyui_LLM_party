import configparser
import json
import locale
import os
from pathlib import Path
from typing import Any


DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent / "MiniMax-H3" / "skills"

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".js",
    ".ts",
    ".csv",
}

MAX_TEXT_CHARS = 80_000

# Every root a MiniMaxH3SkillsTool node has published tools for, in registration
# order. Tool calls arrive without node context, so a skill name is resolved
# against all of them rather than against a single "last node wins" global.
_REGISTERED_ROOTS: list[Path] = []


def _register_root(root: Path) -> None:
    if root not in _REGISTERED_ROOTS:
        _REGISTERED_ROOTS.append(root)


def _search_roots() -> list[Path]:
    return _REGISTERED_ROOTS or [DEFAULT_SKILLS_ROOT]


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Read the leading YAML frontmatter of a SKILL file without PyYAML."""
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        return {}

    try:
        end_index = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}

    header = lines[1:end_index]
    metadata: dict[str, str] = {}

    index = 0
    while index < len(header):
        line = header[index]

        if line.startswith("name:"):
            metadata["name"] = line.split(":", 1)[1].strip().strip("'\"")

        elif line.startswith("description:"):
            value = line.split(":", 1)[1].strip()

            if value in {"|", ">"}:
                block, index = _read_block_scalar(header, index + 1)
                metadata["description"] = block
                continue

            metadata["description"] = value.strip("'\"")

        index += 1

    return metadata


def _read_block_scalar(header: list[str], start: int) -> tuple[str, int]:
    """
    Collect an indented YAML block scalar, returning its text and the index of
    the first line that is not part of it.

    A block scalar ends at the first non-blank line that is not indented. Testing
    indentation alone — rather than also looking for a colon — keeps prose lines
    such as "note: keep the aspect ratio" inside the description where they
    belong.
    """
    collected: list[str] = []
    index = start

    while index < len(header):
        line = header[index]

        if line.strip() and not line.startswith((" ", "\t")):
            break

        collected.append(line.strip())
        index += 1

    return " ".join(part for part in collected if part), index


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _resolve_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()

    if not resolved.is_dir():
        raise FileNotFoundError(f"MiniMax H3 skills 目录不存在：{root}")

    return resolved


def discover_skills(root: Path) -> dict[str, dict[str, Any]]:
    """
    Scan root/*/SKILL.md for skills.

    Skills are keyed by their frontmatter name rather than their folder name, so
    a folder such as mv-subtitle-skill-confirmed registers as
    music-video-subtitle-generator.
    """
    resolved = _resolve_root(root)
    registry: dict[str, dict[str, Any]] = {}

    for folder in sorted(resolved.iterdir()):
        if not folder.is_dir():
            continue

        en_file = folder / "SKILL.md"
        cn_file = folder / "SKILL.cn.md"

        if not en_file.exists() and not cn_file.exists():
            continue

        en_meta = _parse_frontmatter(_read_text(en_file)) if en_file.exists() else {}
        cn_meta = _parse_frontmatter(_read_text(cn_file)) if cn_file.exists() else {}

        skill_name = en_meta.get("name") or cn_meta.get("name") or folder.name

        if skill_name in registry:
            raise ValueError(
                f"技能名称重复：{skill_name!r} 同时来自 "
                f"{registry[skill_name]['folder'].name} 和 {folder.name}。"
                "请修改其中一个 SKILL 文件的 frontmatter name。"
            )

        # Chinese conversations are the common case, so prefer the Chinese blurb.
        description = (
            cn_meta.get("description")
            or en_meta.get("description")
            or f"MiniMax H3 skill: {skill_name}"
        )

        registry[skill_name] = {
            "name": skill_name,
            "description": description,
            "folder": folder,
            "en_file": en_file if en_file.exists() else None,
            "cn_file": cn_file if cn_file.exists() else None,
        }

    return registry


def _get_skill(skill_name: str) -> dict[str, Any]:
    available: set[str] = set()

    for root in _search_roots():
        try:
            registry = discover_skills(root)
        except (OSError, ValueError):
            continue

        if skill_name in registry:
            return registry[skill_name]

        available.update(registry)

    raise ValueError(
        f"找不到技能 {skill_name!r}。可用技能：{', '.join(sorted(available)) or '无'}"
    )


def _list_text_resources(skill_folder: Path) -> list[str]:
    resources: list[str] = []

    for path in sorted(skill_folder.rglob("*")):
        if not path.is_file():
            continue

        if path.name in {"SKILL.md", "SKILL.cn.md"}:
            continue

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        resources.append(path.relative_to(skill_folder).as_posix())

    return resources


def _truncate(content: str, label: str) -> str:
    if len(content) <= MAX_TEXT_CHARS:
        return content

    return content[:MAX_TEXT_CHARS] + f"\n\n[{label}因长度限制被截断]"


def load_h3_skill(skill_name: str, task: str, language: str = "auto") -> str:
    """Load a full skill document. Invoked by LLM-Party's dispatch_tool."""
    skill = _get_skill(skill_name)

    language = str(language or "auto").lower()

    if language in {"en", "english"}:
        selected_file = skill["en_file"] or skill["cn_file"]
    else:
        selected_file = skill["cn_file"] or skill["en_file"]

    if selected_file is None:
        return f"技能 {skill_name} 没有可读取的 SKILL 文件。"

    content = _truncate(_read_text(selected_file), "SKILL 内容")

    resources = _list_text_resources(skill["folder"])
    resources_text = (
        "\n".join(f"- {item}" for item in resources) if resources else "无额外文本资源"
    )

    return f"""
已加载 MiniMax H3 Skill。

技能名称：
{skill_name}

技能文件：
{selected_file.name}

用户当前任务：
<user_task>
{task}
</user_task>

技能正文：
<skill_document>
{content}
</skill_document>

该技能目录中的可读取文本资源：
<available_resources>
{resources_text}
</available_resources>

执行要求：

1. 严格按照 skill_document 的流程、Gate 和输出规则执行。
2. 如果技能正文明确要求阅读 references 中的文件，
   必须调用 read_h3_skill_resource。
3. 不要虚构尚未读取的 reference 内容。
4. 不要只总结技能，应使用技能完成用户任务。
5. 已经读取过的技能和资源不要重复读取。
""".strip()


def read_h3_skill_resource(skill_name: str, relative_path: str) -> str:
    """Read a references file or other text resource inside a skill folder."""
    skill = _get_skill(skill_name)
    skill_folder = skill["folder"].resolve()

    relative_path = str(relative_path).strip()
    target = (skill_folder / relative_path).resolve()

    try:
        target.relative_to(skill_folder)
    except ValueError:
        return "拒绝读取：资源路径超出了技能目录。"

    if not target.is_file():
        available = _list_text_resources(skill_folder)
        return (
            f"资源不存在：{relative_path}\n"
            f"可用文本资源：{json.dumps(available, ensure_ascii=False)}"
        )

    if target.suffix.lower() not in TEXT_EXTENSIONS:
        return f"资源 {relative_path} 不是受支持的文本文件，无法注入文本对话。"

    content = _truncate(_read_text(target), "资源内容")

    return f"""
已读取技能资源。

技能：
{skill_name}

资源：
{relative_path}

<skill_resource>
{content}
</skill_resource>

请继续按照已加载 Skill 执行用户任务。
不要只复述该资源。
""".strip()


class MiniMaxH3SkillsTool:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "skills_root": (
                    "STRING",
                    {
                        "default": str(DEFAULT_SKILLS_ROOT),
                        "multiline": False,
                        "tooltip": "MiniMax-H3 仓库中的 skills 目录",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)
    FUNCTION = "build_tools"
    CATEGORY = "大模型派对（llm_party）/工具（tools）/技能（Skills）"

    def build_tools(self, skills_root: str, is_enable: bool = True):
        if not is_enable:
            return (None,)

        root = _resolve_root(Path(os.path.expandvars(skills_root)))
        registry = discover_skills(root)

        if not registry:
            raise RuntimeError(f"目录中没有发现 SKILL.md：{skills_root}")

        _register_root(root)

        skill_names = sorted(registry)
        catalog = "\n".join(
            f"- {name}: {registry[name]['description']}" for name in skill_names
        )

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "load_h3_skill",
                    "description": (
                        "加载最适合当前任务的 MiniMax H3 Skill。"
                        "当用户请求与下列技能之一明确匹配时调用。"
                        "普通问答不要调用。调用后必须遵循技能正文，"
                        "并按需读取其 references。"
                        "\n\n可用技能：\n" + catalog
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "skill_name": {
                                "type": "string",
                                "enum": skill_names,
                                "description": "需要加载的技能名称",
                            },
                            "task": {
                                "type": "string",
                                "description": (
                                    "用户当前的完整任务。"
                                    "必须保留素材、时长、比例、"
                                    "风格和输出要求等约束。"
                                ),
                            },
                            "language": {
                                "type": "string",
                                "enum": ["auto", "zh", "en"],
                                "description": "技能文档语言。中文用户优先 zh。",
                                "default": "auto",
                            },
                        },
                        "required": ["skill_name", "task"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_h3_skill_resource",
                    "description": (
                        "读取已经加载的 MiniMax H3 Skill "
                        "目录中的 references 或其他文本资源。"
                        "只有 SKILL 正文明确要求读取某个资源时调用。"
                        "一次只读取一个文件。"
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "skill_name": {
                                "type": "string",
                                "enum": skill_names,
                                "description": "已加载的技能名称",
                            },
                            "relative_path": {
                                "type": "string",
                                "description": (
                                    "相对于技能目录的资源路径，"
                                    "例如 references/base-en.txt"
                                ),
                            },
                        },
                        "required": ["skill_name", "relative_path"],
                        "additionalProperties": False,
                    },
                },
            },
        ]

        return (json.dumps(tools, ensure_ascii=False),)


_TOOL_HOOKS = ["load_h3_skill", "read_h3_skill_resource"]
NODE_CLASS_MAPPINGS = {"MiniMaxH3SkillsTool": MiniMaxH3SkillsTool}

lang = locale.getlocale()[0]
if lang is not None and "Chinese" in lang:
    lang = "zh_CN"
else:
    lang = "en_US"

config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.ini"
)
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except Exception:
    language = ""
if language in {"zh_CN", "en_US"}:
    lang = language

if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"MiniMaxH3SkillsTool": "MiniMax H3 技能工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"MiniMaxH3SkillsTool": "MiniMax H3 Skills Tool"}
