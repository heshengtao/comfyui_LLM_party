from .install import (
    check_and_uninstall_websocket,
    copy_js_files,
    get_system_info,
    init_temp,
    install_llama,
    install_portaudio,
    manage_discord_packages,
)
from .llm import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

install_portaudio()
copy_js_files()
system_info = get_system_info()
install_llama(system_info)
check_and_uninstall_websocket()
init_temp()
manage_discord_packages()
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
