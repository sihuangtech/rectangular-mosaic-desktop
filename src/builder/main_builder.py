"""
主构建器模块
整合所有构建功能，提供统一的构建接口
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .config_manager import BuildConfig
from .pyinstaller_runner import PyInstallerRunner
from .platform_handler import PlatformHandler
from .utils import get_architecture_choice


class MainBuilder:
    """主构建器"""
    
    def __init__(self):
        self.config = BuildConfig()
        self.runner = None
        self.handler = None
    
    def run(self):
        """运行完整的构建流程"""
        print(f'检测到当前平台：{self.config.current_os} ({self.config.current_arch})')
        
        # 架构选择
        target_arch = get_architecture_choice()
        if target_arch is None:
            print("用户选择退出打包")
            return False
        
        if target_arch == 'auto':
            self.config.target_arch = self.config.current_arch
            print(f'使用当前系统架构：{self.config.target_arch}')
        else:
            self.config.target_arch = target_arch
            print(f'目标架构：{self.config.target_arch}')
            
            # 检查跨架构打包的可行性
            if self.config.target_arch != self.config.current_arch:
                print(f'⚠️  警告：您正在尝试跨架构打包 ({self.config.current_arch} -> {self.config.target_arch})')
                print('这可能需要额外的工具链支持：')
                if (self.config.current_os == 'Darwin' and 
                    self.config.current_arch == 'x86_64' and 
                    self.config.target_arch == 'arm64'):
                    print('- 需要安装 Rosetta 2')
                    print('- 可能需要使用 conda 或特定 Python 环境')
                elif (self.config.current_os == 'Darwin' and 
                      self.config.current_arch == 'arm64' and 
                      self.config.target_arch == 'x86_64'):
                    print('- 需要安装 Rosetta 2')
                
                from .utils import ask_yes_no
                if not ask_yes_no("是否继续跨架构打包?", default='n'):
                    print("已取消打包")
                    return False
        
        # 平台特定的打包格式选择
        self.handler = PlatformHandler(self.config)
        package_choice = self.handler.get_platform_choice()
        if package_choice is None:
            print("用户选择退出打包")
            return False
        
        # 构建前处理
        if not self.handler.handle_pre_build():
            return False
        
        # 配置应用
        if not self._configure_application():
            return False
        
        # 显示配置
        self.config.display_config()
        if self.handler.package_choice:
            print(f'打包格式：{self.handler.get_format_description()}')
        
        # 运行 PyInstaller
        if not self._run_pyinstaller():
            return False
        
        # 构建后处理
        return self._handle_post_build()
    
    def _configure_application(self):
        """配置应用设置"""
        # 应用名称
        if not self.config.configure_app_name():
            return False
        
        # 打包模式
        if not self.config.configure_pack_mode():
            return False
        
        # 窗口模式
        if not self.config.configure_window_mode():
            return False
        
        # 图标配置
        if not self.config.configure_icon():
            return False
        
        return True
    
    def _run_pyinstaller(self):
        """运行 PyInstaller"""
        from .utils import ask_yes_no
        if not ask_yes_no("确认开始打包?", default='y'):
            print("已取消打包")
            return False
        
        self.runner = PyInstallerRunner(self.config)
        return self.runner.run()
    
    def _handle_post_build(self):
        """处理构建后操作"""
        app_name = self.config.get_final_app_name()
        
        if self.config.current_os == 'Darwin':
            app_path = f'dist/{app_name}.app'
            if os.path.exists(app_path):
                return self.handler.handle_post_build(app_name, app_path)
        elif self.config.current_os == 'Linux':
            elf_path = f'dist/{app_name}'
            if os.path.exists(elf_path):
                return self.handler.handle_post_build(app_name, elf_path)
        
        print('\n打包完成！可执行文件在 dist 目录下。')
        print(f'生成的文件适用于 {self.config.current_os} ({self.config.target_arch}) 平台')
        return True


def main():
    """主函数"""
    builder = MainBuilder()
    try:
        success = builder.run()
        if success:
            print("\n✅ 构建成功完成！")
        else:
            print("\n❌ 构建失败或被取消")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户中断构建")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建过程中出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()