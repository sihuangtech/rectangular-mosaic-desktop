"""
PyInstaller 运行器模块
负责执行 PyInstaller 打包命令
"""
import os
import sys
import subprocess
from .config_manager import BuildConfig


class PyInstallerRunner:
    """PyInstaller 运行器"""
    
    def __init__(self, config: BuildConfig):
        self.config = config
        self.args = []
    
    def check_pyinstaller(self):
        """检查 PyInstaller 是否已安装"""
        try:
            import PyInstaller  # noqa: F401
            return True
        except ImportError:
            print('未检测到 pyinstaller，请先运行：pip install pyinstaller')
            return False
    

    
    def build_args(self):
        """构建 PyInstaller 参数"""
        self.args = ['pyinstaller']
        
        # 添加架构指定参数
        if self.config.target_arch == 'x86_64':
            self.args += ['--target-arch', 'x86_64']
        elif self.config.target_arch == 'arm64':
            self.args += ['--target-arch', 'arm64']
        
        # 自动集成 assets 资源目录
        assets_dir = 'assets'
        if os.path.exists(assets_dir):
            separator = self.config.platform_configs['separator']
            self.args += ['--add-data', f'{assets_dir}{separator}{assets_dir}']
        
        # 设置应用名称（含架构后缀）
        final_name = self.config.get_final_app_name()
        self.args += ['--name', final_name]
        
        # 打包模式
        if self.config.pack_mode == 'onefile':
            self.args.append('--onefile')
        
        # 窗口模式
        if self.config.window_mode == 'windowed':
            self.args.append(self.config.platform_configs['window_flag'])
        else:
            self.args.append(self.config.platform_configs['console_flag'])
        
        # 图标
        if self.config.use_icon and self.config.icon_path:
            self.args += ['--icon', self.config.icon_path]
        
        # 自动确认删除已存在的输出目录
        self.args.append('--noconfirm')
        
        # 添加版本信息（macOS 专用）
        if self.config.current_os == 'Darwin':
            from ..constants.config import MAC_PACKAGE_NAME
            # 设置 macOS 应用版本信息
            self.args += ['--osx-bundle-identifier', MAC_PACKAGE_NAME]
        
        # 主脚本
        self.args.append(self.config.main_script)
        
        return self.args
    
    def run(self):
        """运行 PyInstaller"""
        if not self.check_pyinstaller():
            return False
        
        self.build_args()
        
        print('\n=== PyInstaller 配置 ===')
        print('运行命令：', ' '.join(self.args))
        
        try:
            result = subprocess.run(self.args, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"PyInstaller 打包失败: {e}")
            return False
        except Exception as e:
            print(f"运行 PyInstaller 时出错: {e}")
            return False