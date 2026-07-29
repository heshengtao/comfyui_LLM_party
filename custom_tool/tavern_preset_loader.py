import configparser
import json
import locale
import os
import re

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")

_PRESETS_DIR = os.path.join(current_dir, "tavern_presets")


def _scan_presets():
    files = ["(none)"]
    if os.path.isdir(_PRESETS_DIR):
        for f in sorted(os.listdir(_PRESETS_DIR)):
            if f.lower().endswith(".json"):
                files.append(f)
    return files


def _replace_vars(text, char_name, user_name, char_description):
    if not text:
        return text
    text = text.replace("{{char}}", char_name)
    text = text.replace("{{user}}", user_name)
    text = text.replace("{{description}}", char_description)
    text = text.replace("{{personality}}", "")
    text = text.replace("{{scenario}}", "")
    text = text.replace("{{mesExamples}}", "")
    text = text.replace("{{original}}", "")
    text = re.sub(r"\{\{[^}]+\}\}", "", text)
    return text.strip()


class TavernPresetLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "preset_file": (_scan_presets(), {
                    "default": "(none)",
                    "tooltip": "Select a preset JSON from tavern_presets/ folder.",
                }),
            },
            "optional": {
                "char_name": ("STRING", {"default": "char", "tooltip": "Character name, replaces {{char}}."}),
                "user_name": ("STRING", {"default": "user", "tooltip": "User name, replaces {{user}}."}),
                "char_description": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Character description, replaces {{description}}.",
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("system_prompt", "injection_prompts", "assistant_prefill")
    OUTPUT_TOOLTIPS = (
        "System prompt (RELATIVE prompts before chatHistory marker).",
        "JSON array of injectable prompts [{role, content, depth, order}].",
        "Assistant prefill text.",
    )
    FUNCTION = "load_preset"
    CATEGORY = "大模型派对（llm_party）/酒馆增强（tavern）"

    def load_preset(self, preset_file, char_name="char", user_name="user", char_description=""):
        raw_json = ""
        if preset_file and preset_file != "(none)":
            filepath = os.path.join(_PRESETS_DIR, preset_file)
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    raw_json = f.read()

        if not raw_json:
            return ("", "[]", "")

        try:
            preset = json.loads(raw_json)
        except (json.JSONDecodeError, TypeError):
            return ("", "[]", "")

        prompts = preset.get("prompts", [])
        prompt_order_raw = preset.get("prompt_order", [])

        # --- Parse prompt_order: extract [{identifier, enabled}] ---
        ordered_entries = []
        if prompt_order_raw:
            first = prompt_order_raw[0]
            if isinstance(first, dict):
                for entry in first.get("order", []):
                    if isinstance(entry, dict):
                        ordered_entries.append({
                            "identifier": entry.get("identifier", ""),
                            "enabled": entry.get("enabled", True),
                        })
            elif isinstance(first, list):
                for ident in first:
                    ordered_entries.append({"identifier": ident, "enabled": True})
            elif isinstance(first, str):
                for ident in prompt_order_raw:
                    ordered_entries.append({"identifier": ident, "enabled": True})

        # --- Build prompt map from prompts array ---
        prompt_map = {}
        for p in prompts:
            ident = p.get("identifier", p.get("name", ""))
            if ident:
                prompt_map[ident] = p

        if not ordered_entries:
            for p in prompts:
                ident = p.get("identifier", "")
                if ident:
                    ordered_entries.append({"identifier": ident, "enabled": True})

        # --- Find chatHistory marker position ---
        chat_history_idx = None
        for i, entry in enumerate(ordered_entries):
            if entry["identifier"] == "chatHistory":
                chat_history_idx = i
                break

        # --- Process each prompt entry ---
        system_parts = []
        injection_list = []
        assistant_prefill = ""

        for idx, entry in enumerate(ordered_entries):
            ident = entry["identifier"]
            if not entry.get("enabled", True):
                continue

            p = prompt_map.get(ident)
            if not p:
                continue
            if p.get("marker", False):
                continue

            if ident.lower() == "assistantprefill":
                prefill_content = p.get("content", "")
                if prefill_content:
                    assistant_prefill = _replace_vars(prefill_content, char_name, user_name, char_description)
                continue

            content = p.get("content", "")
            if not content or not content.strip():
                continue

            content = _replace_vars(content, char_name, user_name, char_description)
            role = p.get("role", "system")
            injection_position = p.get("injection_position", 0)
            injection_depth = p.get("injection_depth", 4)
            injection_order = p.get("injection_order", 100)

            if injection_position == 1:
                injection_list.append({
                    "role": role,
                    "content": content,
                    "depth": injection_depth,
                    "order": injection_order,
                })
            elif injection_position == 0:
                if chat_history_idx is not None and idx > chat_history_idx:
                    injection_list.append({
                        "role": role,
                        "content": content,
                        "depth": 0,
                        "order": -1,
                    })
                else:
                    system_parts.append(content)

        system_prompt = "\n\n".join(system_parts)
        injection_json = json.dumps(injection_list, ensure_ascii=False)

        return (system_prompt, injection_json, assistant_prefill)


NODE_CLASS_MAPPINGS = {"TavernPresetLoader": TavernPresetLoader}

lang = "zh_CN"
try:
    system_lang = locale.getlocale()[0]
    if system_lang and system_lang.lower().startswith("en"):
        lang = "en_US"
except Exception:
    pass

config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language in ("zh_CN", "en_US"):
    lang = language

if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"TavernPresetLoader": "酒馆预设加载器"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"TavernPresetLoader": "SillyTavern Preset Loader"}
