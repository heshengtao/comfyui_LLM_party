from .install import (
    check_and_uninstall_websocket,
    copy_js_files,
    get_system_info,
    init_temp,
    install_llama,
)
from .llm import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

copy_js_files()
system_info = get_system_info()
install_llama(system_info)
check_and_uninstall_websocket()
init_temp()
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
