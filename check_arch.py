# -*- coding: utf-8 -*-
"""
架构检测工具

用途：
    检测当前系统架构和Python程序架构信息
    帮助用户了解跨架构运行的情况

使用方法：
    python check_arch.py
"""
import platform
import sys
import os
import struct

def check_system_architecture():
    """检测系统架构信息"""
    print("=== 系统架构信息 ===")
    print(f"操作系统: {platform.system()}")
    print(f"系统版本: {platform.release()}")
    print(f"机器类型: {platform.machine()}")
    print(f"处理器: {platform.processor()}")
    print(f"Python架构: {platform.architecture()}")
    print(f"Python位数: {struct.calcsize('P') * 8}位")
    
    # 检测是否支持ARM64模拟
    if platform.system() == "Windows":
        print("\n=== Windows ARM64支持 ===")
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            is_arm64_supported = hasattr(kernel32, 'IsWow64Process2')
            print(f"支持ARM64模拟: {'是' if is_arm64_supported else '否'}")
        except:
            print("无法检测ARM64支持状态")
    
    elif platform.system() == "Darwin":
        print("\n=== macOS ARM64支持 ===")
        try:
            result = os.popen('uname -m').read().strip()
            print(f"当前架构: {result}")
            if result == "x86_64":
                print("检测到Intel Mac，可能通过Rosetta 2运行ARM64程序")
        except:
            print("无法检测架构信息")

def check_python_environment():
    """检测Python环境信息"""
    print("\n=== Python环境信息 ===")
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"Python架构: {platform.architecture()[0]}")
    
    # 检测PySide6架构
    try:
        import PySide6
        print(f"PySide6版本: {PySide6.__version__}")
        print(f"PySide6路径: {PySide6.__file__}")
    except ImportError:
        print("PySide6未安装")

def check_executable_architecture(executable_path):
    """检测可执行文件的架构"""
    if not os.path.exists(executable_path):
        print(f"文件不存在: {executable_path}")
        return
    
    print(f"\n=== 可执行文件架构检测: {executable_path} ===")
    
    if platform.system() == "Windows":
        try:
            import pefile
            pe = pefile.PE(executable_path)
            machine = pe.FILE_HEADER.Machine
            if machine == 0x014c:
                print("架构: x86 (32位)")
            elif machine == 0x8664:
                print("架构: x86_64 (64位)")
            elif machine == 0xaa64:
                print("架构: ARM64")
            else:
                print(f"未知架构: 0x{machine:04x}")
        except ImportError:
            print("需要安装pefile库: pip install pefile")
        except Exception as e:
            print(f"检测失败: {e}")
    
    elif platform.system() == "Darwin":
        try:
            result = os.popen(f'file {executable_path}').read().strip()
            print(f"文件信息: {result}")
        except Exception as e:
            print(f"检测失败: {e}")
    
    elif platform.system() == "Linux":
        try:
            result = os.popen(f'file {executable_path}').read().strip()
            print(f"文件信息: {result}")
        except Exception as e:
            print(f"检测失败: {e}")

def main():
    """主函数"""
    print("架构检测工具")
    print("=" * 50)
    
    # 检测系统架构
    check_system_architecture()
    
    # 检测Python环境
    check_python_environment()
    
    # 检测打包后的可执行文件（如果存在）
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        print(f"\n=== 检测dist目录下的可执行文件 ===")
        for file in os.listdir(dist_dir):
            file_path = os.path.join(dist_dir, file)
            if os.path.isfile(file_path):
                # 检查是否是可执行文件
                if (file.endswith('.exe') or 
                    file.endswith('.app') or 
                    (not file.endswith('.dmg') and not file.endswith('.pkg') and not file.endswith('.deb') and not file.endswith('.rpm'))):
                    check_executable_architecture(file_path)
    
    print("\n=== 总结 ===")
    print("如果您能在x86_64系统上运行ARM64程序，可能是因为：")
    print("1. 操作系统提供了架构模拟功能")
    print("2. 程序实际是通用二进制文件")
    print("3. 使用了跨架构兼容的运行时库")
    print("\n建议：")
    print("- 使用本工具检测具体的架构信息")
    print("- 在目标架构的系统上测试程序性能")
    print("- 考虑为不同架构分别打包以获得最佳性能")

if __name__ == "__main__":
    main() 