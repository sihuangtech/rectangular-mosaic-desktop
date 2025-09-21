"""
配置管理模块
处理打包配置和用户交互
"""
import os
import platform
from .utils import ask_yes_no, detect_current_arch


class BuildConfig:
    """构建配置管理器"""
    
    def __init__(self):
        self.current_os = platform.system()
        self.current_arch = detect_current_arch()
        self.target_arch = 'auto'
        self.app_name = 'Rect Mosaic'
        self.main_script = 'main.py'
        self.pack_mode = 'onedir'  # 'onedir' or 'onefile'
        self.window_mode = 'windowed'  # 'console' or 'windowed'
        self.use_icon = True
        self.icon_path = None
        self.platform_configs = self._get_platform_configs()
    
    def _get_platform_configs(self):
        """获取平台相关配置"""
        configs = {
            'Windows': {
                'icon': 'assets/icons/app.ico',
                'separator': ';',
                'console_flag': '--noconsole',
                'window_flag': '--noconsole'
            },
            'Darwin': {
                'icon': 'assets/icons/app.icns',
                'separator': ':',
                'console_flag': '--console',
                'window_flag': '--windowed'
            },
            'Linux': {
                'icon': 'assets/icons/app.png',
                'separator': ':',
                'console_flag': '--console',
                'window_flag': '--windowed'
            }
        }
        return configs.get(self.current_os, configs['Linux'])
    
    def get_icon_path(self):
        """获取图标路径"""
        default_icon = self.platform_configs['icon']
        if os.path.exists(default_icon):
            return default_icon
        return None
    
    def configure_app_name(self):
        """配置应用名称"""
        print("\n=== 应用名称设置 ===")
        print(f"默认应用名称: {self.app_name}")
        print("输入 'q' 或 'quit' 退出打包")
        
        while True:
            name_input = input(f"是否使用默认应用名称 '{self.app_name}'? (y/n, 默认y): ").strip().lower()
            if name_input in ['q', 'quit']:
                return False
            if not name_input:
                name_input = 'y'
            
            if name_input in ['y', 'yes']:
                return True
            elif name_input in ['n', 'no']:
                custom_name = input("请输入应用名称: ").strip()
                if not custom_name:
                    print("应用名称不能为空，使用默认名称")
                    return True
                else:
                    self.app_name = custom_name
                    return True
            else:
                print("无效输入，请输入 y 或 n")
    
    def configure_pack_mode(self):
        """配置打包模式"""
        print("\n=== 打包模式选择 ===")
        print("1. 目录模式 (--onedir) - 生成包含多个文件的文件夹 (默认)")
        print("2. 单文件模式 (--onefile) - 生成单个可执行文件")
        print("输入 'q' 或 'quit' 退出打包")
        
        while True:
            pack_mode = input("请选择打包模式 (1/2, 默认1): ").strip()
            if pack_mode in ['q', 'quit']:
                return False
            if not pack_mode:
                pack_mode = '1'
            
            if pack_mode == '1':
                self.pack_mode = 'onedir'
                return True
            elif pack_mode == '2':
                self.pack_mode = 'onefile'
                return True
            else:
                print("无效选择，请输入 1 或 2")
    
    def configure_window_mode(self):
        """配置窗口模式"""
        print("\n=== 窗口模式选择 ===")
        print("输入 'q' 或 'quit' 退出打包")
        
        if self.current_os == 'Windows':
            print("1. 控制台模式 - 显示控制台窗口")
            print("2. 窗口模式 - 隐藏控制台窗口 (默认)")
        else:
            print("1. 控制台模式 - 显示终端窗口")
            print("2. 窗口模式 - 隐藏终端窗口 (默认)")
        
        win_mode = input("请选择窗口模式 (1/2, 默认2): ").strip()
        if win_mode in ['q', 'quit']:
            return False
        if not win_mode or win_mode == '2':
            self.window_mode = 'windowed'
        elif win_mode == '1':
            self.window_mode = 'console'
        else:
            print("无效选择，使用默认窗口模式")
            self.window_mode = 'windowed'
        
        return True
    
    def configure_icon(self):
        """配置图标"""
        default_icon = self.get_icon_path()
        if ask_yes_no(f"是否添加图标 (--icon)? [{'Y' if default_icon else 'n'}]", 
                     default='y' if default_icon else 'n'):
            if default_icon:
                self.icon_path = default_icon
                self.use_icon = True
            else:
                icon_path = input("请输入图标文件路径: ").strip()
                if icon_path and os.path.exists(icon_path):
                    self.icon_path = icon_path
                    self.use_icon = True
                else:
                    print('未找到有效图标文件，将不使用图标')
                    self.use_icon = False
        else:
            self.use_icon = False
        
        return True
    
    def get_final_app_name(self):
        """获取最终的应用名称（含架构后缀）"""
        if self.current_os == 'Windows' and self.target_arch and self.target_arch != 'auto':
            return f"{self.app_name}-{self.target_arch}"
        return self.app_name
    
    def display_config(self):
        """显示当前配置"""
        print('\n=== 构建配置 ===')
        print(f'目标平台：{self.current_os}')
        print(f'目标架构：{self.target_arch}')
        print(f'应用名称：{self.app_name}')
        print(f'打包模式：{self.pack_mode}')
        print(f'窗口模式：{self.window_mode}')
        print(f'使用图标：{self.use_icon}')
        if self.use_icon and self.icon_path:
            print(f'图标路径：{self.icon_path}')