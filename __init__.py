from .llm import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from .install import copy_js_files,get_system_info,install_llama,check_and_uninstall_websocket

copy_js_files()
system_info = get_system_info()
install_llama(system_info)
check_and_uninstall_websocket()
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
