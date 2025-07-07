# -*- coding: utf-8 -*-
"""
交互式参数选择 + 自动平台检测 PyInstaller 打包脚本

用途：
    自动检测当前操作系统，打包参数由用户运行时选择。
    只能打包本平台可执行文件，不能跨平台打包。

使用方法：
    python build_exe.py
"""
import sys
import subprocess
import platform
import os

MAIN_SCRIPT = 'main.py'

def ask_yes_no(prompt, default='y'):
    ans = input(f"{prompt} (y/n, 默认{default}): ").strip().lower()
    if not ans:
        ans = default
    return ans == 'y'

def main():
    current_os = platform.system()
    if current_os == 'Windows':
        print('检测到当前平台：Windows，将打包为 .exe 可执行文件')
        default_icon = 'assets/icons/app.ico'
    elif current_os == 'Darwin':
        print('检测到当前平台：Mac OSX，将打包为 .app 可执行文件')
        default_icon = 'assets/icons/app.icns'
    elif current_os == 'Linux':
        print('检测到当前平台：Linux，将打包为 ELF 可执行文件')
        default_icon = 'assets/icons/app.png'
    else:
        print(f'不支持的操作系统：{current_os}，已退出。')
        return

    args = ['pyinstaller']

    # 自动集成 assets/icons 资源目录
    icons_dir = 'assets/icons'
    if os.path.exists(icons_dir):
        sep = ';' if current_os == 'Windows' else ':'
        args += ['--add-data', f'{icons_dir}{sep}{icons_dir}']

    # 交互式参数选择
    if ask_yes_no("是否打包为单一文件 (--onefile)?"):
        args.append('--onefile')
    if current_os == 'Windows':
        if ask_yes_no("是否关闭控制台窗口 (--noconsole)?"):
            args.append('--noconsole')
    else:
        if ask_yes_no("是否以 GUI 模式打包 (--windowed)?"):
            args.append('--windowed')

    icon_exists = os.path.exists(default_icon)
    if ask_yes_no(f"是否添加图标 (--icon)? [{'Y' if icon_exists else 'n'}]", default='y' if icon_exists else 'n'):
        icon_path = default_icon if icon_exists else input("请输入 .ico 或 .icns 图标文件路径: ").strip()
        if icon_path and os.path.exists(icon_path):
            args += ['--icon', icon_path]
        elif not icon_exists:
            print('未检测到默认图标文件，请手动输入有效路径。')

    args.append(MAIN_SCRIPT)

    # 检查 pyinstaller 是否已安装
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print('未检测到 pyinstaller，请先运行：pip install pyinstaller')
        sys.exit(1)

    print('运行命令：', ' '.join(args))
    subprocess.run(args)
    print('\n打包完成！可执行文件在 dist 目录下。')

if __name__ == "__main__":
    main() 