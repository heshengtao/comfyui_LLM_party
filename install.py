import os
import shutil


def copy_js_files():
    # 设置当前文件夹路径和目标文件夹路径
    current_folder = os.path.dirname(os.path.abspath(__file__))
    target_folder = os.path.join("web/extensions/party")

    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 获取当前文件夹中web子文件夹下的所有.js文件
    js_files = [f for f in os.listdir(os.path.join(current_folder, "web")) if f.endswith(".js")]

    # 复制文件
    for file_name in js_files:
        source_file = os.path.join(current_folder, "web", file_name)
        target_file = os.path.join(target_folder, file_name)
        shutil.copy2(source_file, target_file)
        print(f"复制了文件: {file_name}")


# 调用函数
copy_js_files()
