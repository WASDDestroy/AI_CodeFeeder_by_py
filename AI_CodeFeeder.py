#AI_CodeFeeder V1.0.8 (Config Loaded)
#Coded by ChaoPhone 2026.1.18

import os
import sys
import json
import tkinter as tk
from tkinter import filedialog
import subprocess

# --- 配置区域 (已修改为读取 config.json) ---

# 1. 确定配置文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.json')

# 2. 读取配置
if not os.path.exists(config_path):
    print(f"❌ 错误：找不到配置文件 config.json")
    print(f"请确保文件位于: {current_dir}")
    input("按回车键退出...")
    sys.exit(1)

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except Exception as e:
    print(f"❌ 配置文件格式错误: {e}")
    sys.exit(1)

# 3. 映射变量 (注意类型转换)
# Set 用于快速查找 (O(1))
ALLOWED_EXTENSIONS = set(config_data.get('allowed_extensions', []))
IGNORE_DIRS = set(config_data.get('ignore_dirs', []))
IGNORE_FILES = set(config_data.get('ignore_files', []))

# Tuple 用于 startswith 方法
IGNORE_PREFIXES = tuple(config_data.get('ignore_prefixes', []))

# 4. 强制忽略脚本自身 (防止递归读取)
IGNORE_FILES.add(os.path.basename(__file__))



# --- 核心逻辑  ---

def is_text_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


def get_sorted_file_list(start_path):
    """扫描并返回所有符合条件的文件路径列表"""
    file_list = []
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for f in files:
            # 1. 检查完全匹配的黑名单
            if f in IGNORE_FILES: continue
            if f.endswith('_Codes.md'): continue

            # 2. 检查前缀黑名单
            if any(f.startswith(prefix) for prefix in IGNORE_PREFIXES): continue

            if is_text_file(f):
                rel_path = os.path.relpath(os.path.join(root, f), start_path)
                file_list.append(rel_path)
    return sorted(file_list)


def generate_tree(start_path, files_to_include):
    """生成目录树结构的字符串"""
    tree_str = "# Project Directory Structure\n\n```text\n"
    tree_str += f"{os.path.basename(start_path)}/\n"
    included_set = set(files_to_include)

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        rel_path = os.path.relpath(root, start_path)
        level = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
        indent = ' ' * 4 * level
        subindent = ' ' * 4 * (level + 1)

        if rel_path != '.':
            tree_str += f"{indent}{os.path.basename(root)}/\n"

        for f in files:
            file_rel_path = os.path.relpath(os.path.join(root, f), start_path)
            if file_rel_path in included_set:
                tree_str += f"{subindent}{f}\n"

    tree_str += "```\n\n---\n\n"
    return tree_str


def show_file_in_explorer(path):
    """[Windows专用] 打开资源管理器并选中文件"""
    abs_path = os.path.abspath(path)
    abs_path = os.path.normpath(abs_path)

    print(f"📂 正在打开所在文件夹: {abs_path}")
    try:
        if os.name == 'nt':
            subprocess.Popen(f'explorer /select,"{abs_path}"')
        else:
            print("非 Windows 系统，请手动打开目录。")
    except Exception as e:
        print(f"⚠️ 无法自动打开文件夹: {e}")


def merge_files(start_path, output_path, target_files):
    """执行合并写入"""
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(generate_tree(start_path, target_files))
            print(f"\n正在写入 {len(target_files)} 个文件...")

            for rel_path in target_files:
                full_path = os.path.join(start_path, rel_path)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        outfile.write(f"## File: {rel_path}\n\n")
                        ext = os.path.splitext(rel_path)[1][1:] or 'text'
                        outfile.write(f"```{ext}\n{content}\n```\n\n---\n\n")
                except Exception as e:
                    print(f"读取错误: {rel_path} - {e}")

        print(f"\n✅ 成功！文件已生成: {output_path}")
        show_file_in_explorer(output_path)

    except Exception as e:
        print(f"\n❌ 写入失败: {e}")




if __name__ == "__main__":
    print("-" * 50)
    print("AI_CodeFeeder V1.0.8 (Config Loaded)")
    print("Coded by ChaoPhone 2026.1.18")
    print("-" * 50)

    # --- 初始化 Tkinter ---
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # 1. 选择目录
    print("等待用户选择目标主目录...")
    project_root = filedialog.askdirectory(title="请选择要分析的目标主目录")

    if not project_root:
        print("❌ 未选择目录，程序退出。")
        root.destroy()
    else:
        print("\n🔍 正在预扫描工程...")
        files_to_process = get_sorted_file_list(project_root)

        if not files_to_process:
            print("❌ 未找到符合条件的代码文件。")
            root.destroy()
        else:
            print(f"即将合并以下 {len(files_to_process)} 个文件:")
            for f in files_to_process:
                print(f" [📄] {f}")

            print(f"扫描目标: {project_root}")
            confirm = input("\n按回车键选择保存位置并生成 Markdown，输入 'n' 退出: ")

            if confirm.lower() != 'n':
                default_filename = f"{os.path.basename(project_root)}_Codes.md"

                output_path = filedialog.asksaveasfilename(
                    title="请选择输出文档的位置和名称",
                    initialdir=project_root,
                    initialfile=default_filename,
                    defaultextension=".md",
                    filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
                )

                if output_path:
                    merge_files(project_root, output_path, files_to_process)
                else:
                    print("操作已取消。")
            else:
                print("操作已取消。")

            root.destroy()