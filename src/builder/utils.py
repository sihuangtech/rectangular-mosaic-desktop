"""
构建工具模块 - 通用工具函数
"""
import os
import subprocess
import platform


def detect_current_arch():
    """检测当前系统架构"""
    machine = platform.machine().lower()
    if machine in ['x86_64', 'amd64']:
        return 'x86_64'
    elif machine in ['arm64', 'aarch64']:
        return 'arm64'
    elif machine in ['i386', 'i686']:
        return 'x86'
    else:
        return machine


def ask_yes_no(question, default='y'):
    """询问用户是/否问题"""
    if default == 'y':
        prompt = f"{question} [Y/n]: "
    else:
        prompt = f"{question} [y/N]: "
    
    while True:
        try:
            response = input(prompt).strip().lower()
            if not response:
                return default == 'y'
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("请输入 'y' 或 'n'")
        except (EOFError, KeyboardInterrupt):
            return default == 'y'


def get_architecture_choice():
    """获取用户选择的架构"""
    print("\n=== 架构选择 ===")
    print("1. 自动检测 (默认)")
    print("2. x86_64 (Intel/AMD)")
    print("3. arm64 (Apple Silicon)")
    print("输入 'q' 或 'quit' 退出打包")
    
    while True:
        choice = input("请选择目标架构 (1-3, 默认1): ").strip().lower()
        if choice in ['q', 'quit']:
            return None
        if not choice:
            return 'auto'
        
        if choice == '1':
            return 'auto'
        elif choice == '2':
            return 'x86_64'
        elif choice == '3':
            return 'arm64'
        else:
            print("无效选择，请输入 1-3")


def run_command(cmd, capture_output=True, check=True):
    """运行系统命令"""
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {' '.join(cmd)}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        raise
    except FileNotFoundError:
        print(f"命令未找到: {cmd[0]}")
        raise