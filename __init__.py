from .llm import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from .install import copy_js_files

copy_js_files()

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
