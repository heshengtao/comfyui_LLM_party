"""One-run-delayed pipeline wrapper for LLM Party's API LLM node."""

from __future__ import annotations

import json
import os
import sys
import threading
from typing import Any, Dict, Optional, Tuple


_STATES: Dict[str, Dict[str, Any]] = {}
_LOCK = threading.RLock()


def _history_choices():
    temp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp")
    try:
        paths = [os.path.join(temp_path, name) for name in os.listdir(temp_path)]
        paths = [path for path in paths if os.path.isfile(path)]
        paths.sort(key=os.path.getmtime, reverse=True)
        return [""] + [os.path.basename(path) for path in paths]
    except OSError:
        return [""]


def _new_state(reset_counter: int) -> Dict[str, Any]:
    return {
        "ready": None,
        "ready_seq": 0,
        "running": False,
        "pending": None,
        "delegate": None,
        "error": "",
        "version": 0,
        "last_reset": reset_counter,
    }


def _create_delegate(model):
    """Find the owning llm.py module and instantiate its original LLM node."""
    module_name = model.__class__.__module__
    module = sys.modules.get(module_name)
    llm_class = getattr(module, "LLM", None) if module is not None else None
    if llm_class is None:
        raise RuntimeError(
            "无法定位 comfyui_LLM_party.llm.LLM；请使用本插件的 ☁️API LLM Loader 输出"
        )
    return llm_class()


def _clone_images_to_cpu(images):
    """Detach queued image input from GPU work before the background request starts."""
    if images is None:
        return None
    try:
        return images.detach().cpu().clone()
    except AttributeError:
        return images


def _validate_result(result) -> Tuple[Any, Any, Any, Any, Any]:
    if not isinstance(result, (tuple, list)) or len(result) != 5:
        raise RuntimeError("原 LLM 节点返回了无效结果，预期为 5 路输出")
    response, history, tool, image, reasoning = result
    if response is None:
        raise RuntimeError("原 LLM 节点没有返回 assistant_response")
    if not str(response).strip() and str(reasoning or "").strip():
        raise RuntimeError("LLM 只返回了推理内容而没有最终回答；请提高 max_length")
    if not str(response).strip():
        raise RuntimeError("LLM 最终回答为空；保留上一轮输出")
    return response, history, tool, image, reasoning


def _worker(state_key: str):
    while True:
        with _LOCK:
            state = _STATES.get(state_key)
            if state is None:
                return
            payload = state["pending"]
            state["pending"] = None
            if payload is None:
                state["running"] = False
                return
            version = state["version"]
            delegate = state["delegate"]

        try:
            if delegate is None:
                delegate = _create_delegate(payload["model"])
                with _LOCK:
                    state = _STATES.get(state_key)
                    if state is None:
                        return
                    if state["version"] == version:
                        state["delegate"] = delegate
            result = _validate_result(delegate.chatbot(**payload))
            error: Optional[str] = None
        except Exception as exc:
            result = None
            error = str(exc)

        with _LOCK:
            state = _STATES.get(state_key)
            if state is None:
                return
            if state["version"] == version:
                if result is not None:
                    state["ready"] = result
                    state["ready_seq"] += 1
                    state["error"] = ""
                else:
                    state["error"] = error or "未知错误"
            if state["pending"] is None:
                state["running"] = False
                return


def _start_worker(state_key: str):
    threading.Thread(
        target=_worker,
        args=(state_key,),
        name=f"llm-party-pipeline-{state_key}",
        daemon=True,
    ).start()


class LLMPartyPipeline:
    """Reuse all LLM Party behavior while moving the next request to a background thread."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": "你是一个强大的人工智能助手。"}),
                "user_prompt": ("STRING", {"multiline": True, "default": "你好"}),
                "model": ("CUSTOM",),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "is_memory": (["enable", "disable"], {"default": "disable"}),
                "is_tools_in_sys_prompt": (["enable", "disable"], {"default": "disable"}),
                "is_locked": (["enable", "disable"], {"default": "disable"}),
                "main_brain": (["enable", "disable"], {"default": "enable"}),
                "max_length": ("INT", {"default": 1920, "min": 256, "max": 128000, "step": 128}),
            },
            "optional": {
                "system_prompt_input": ("STRING", {"forceInput": True}),
                "user_prompt_input": ("STRING", {"forceInput": True}),
                "tools": ("STRING", {"forceInput": True}),
                "file_content": ("STRING", {"forceInput": True}),
                "images": ("IMAGE", {"forceInput": True}),
                "imgbb_api_key": ("STRING", {"default": ""}),
                "conversation_rounds": ("INT", {"default": 100, "min": 1, "max": 10000, "step": 1}),
                "historical_record": (_history_choices(), {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "extra_parameters": ("DICT", {"forceInput": True}),
                "user_history": ("STRING", {"forceInput": True}),
                "img_URL": ("STRING", {"forceInput": True}),
                "stream": ("BOOLEAN", {"default": False}),
                "pipeline_first_run": (["使用原始用户提示词", "输出空字符串"],),
                "pipeline_reset": ("INT", {"default": 0, "min": 0, "max": 999999, "step": 1}),
                "pipeline_namespace": ("STRING", {"default": "default"}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "IMAGE", "STRING", "STRING")
    RETURN_NAMES = (
        "assistant_response",
        "history",
        "tool",
        "image",
        "reasoning_content",
        "pipeline_status",
    )
    FUNCTION = "chatbot"
    CATEGORY = "大模型派对（llm_party）/模型链（model_chain）"
    DESCRIPTION = "完整复用 API LLM 通用链路，本轮输出上一轮结果并在后台生成下一轮。"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def chatbot(
        self,
        user_prompt,
        main_brain,
        system_prompt,
        model,
        temperature,
        is_memory,
        is_tools_in_sys_prompt,
        is_locked,
        max_length,
        system_prompt_input="",
        user_prompt_input="",
        tools=None,
        file_content=None,
        images=None,
        imgbb_api_key=None,
        conversation_rounds=100,
        historical_record="",
        is_enable=True,
        extra_parameters=None,
        user_history=None,
        img_URL=None,
        stream=False,
        pipeline_first_run="使用原始用户提示词",
        pipeline_reset=0,
        pipeline_namespace="default",
        unique_id=None,
    ):
        if not is_enable:
            return (None, None, None, None, "", "Pipeline 已禁用")

        node_key = unique_id if unique_id is not None else id(self)
        state_key = f"{str(pipeline_namespace or 'default').strip()}:{node_key}"
        pipeline_reset = int(pipeline_reset or 0)
        payload = {
            "user_prompt": user_prompt,
            "main_brain": main_brain,
            "system_prompt": system_prompt,
            "model": model,
            "temperature": temperature,
            "is_memory": is_memory,
            "is_tools_in_sys_prompt": is_tools_in_sys_prompt,
            "is_locked": is_locked,
            "max_length": max_length,
            "system_prompt_input": system_prompt_input,
            "user_prompt_input": user_prompt_input,
            "tools": tools,
            "file_content": file_content,
            "images": _clone_images_to_cpu(images),
            "imgbb_api_key": imgbb_api_key,
            "conversation_rounds": conversation_rounds,
            "historical_record": historical_record,
            "is_enable": is_enable,
            "extra_parameters": extra_parameters,
            "user_history": user_history,
            "img_URL": img_URL,
            "stream": stream,
        }

        should_start = False
        with _LOCK:
            state = _STATES.get(state_key)
            if state is None:
                state = _new_state(pipeline_reset)
                _STATES[state_key] = state
            elif state["last_reset"] != pipeline_reset:
                state["version"] += 1
                state["ready"] = None
                state["ready_seq"] = 0
                state["pending"] = None
                state["delegate"] = None
                state["error"] = ""
                state["last_reset"] = pipeline_reset

            ready = state["ready"]
            ready_seq = state["ready_seq"]
            previous_error = state["error"]
            was_running = state["running"]
            state["pending"] = payload
            if not state["running"]:
                state["running"] = True
                should_start = True

        if should_start:
            _start_worker(state_key)

        if ready is not None:
            response, history, tool, image, reasoning = ready
            status = f"本轮使用缓存 #{ready_seq}；"
        else:
            combined_user = str(user_prompt or "") + str(user_prompt_input or "")
            response = combined_user if pipeline_first_run == "使用原始用户提示词" else ""
            combined_system = str(system_prompt or "") + str(system_prompt_input or "")
            history = json.dumps([{"role": "system", "content": combined_system}], ensure_ascii=False)
            tool, image, reasoning = "", None, ""
            status = "预热中；"

        status += "后台请求运行中" if was_running else "已提交下一条后台请求"
        if previous_error:
            status += f"；上次错误：{previous_error}"
        return response, history, tool, image, reasoning, status


NODE_CLASS_MAPPINGS = {"LLMPartyPipeline": LLMPartyPipeline}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LLMPartyPipeline": "☁️API LLM Pipeline（上一轮输出）"
}
