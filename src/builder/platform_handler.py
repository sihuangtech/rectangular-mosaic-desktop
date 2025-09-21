"""
平台处理器模块
处理不同平台的打包后处理
"""
import os
from .mac_packager import (
    get_mac_package_format, create_dmg, create_pkg, create_mac_app_store_package
)
from .linux_packager import get_linux_package_format, create_deb, create_rpm
from .config_manager import BuildConfig


class PlatformHandler:
    """平台处理器"""
    
    def __init__(self, config: BuildConfig):
        self.config = config
        self.package_choice = None
    
    def get_platform_choice(self):
        """获取平台的打包格式选择"""
        if self.config.current_os == 'Darwin':
            self.package_choice = get_mac_package_format()
        elif self.config.current_os == 'Linux':
            self.package_choice = get_linux_package_format()
        else:
            self.package_choice = None
        
        return self.package_choice
    
    def handle_pre_build(self):
        """处理构建前的平台相关逻辑"""
        if not self.package_choice:
            return True
        
        if self.config.current_os == 'Darwin':
            return self._handle_mac_pre_build()
        elif self.config.current_os == 'Linux':
            return self._handle_linux_pre_build()
        
        return True
    
    def _handle_mac_pre_build(self):
        """处理Mac平台的构建前逻辑"""
        if self.package_choice in ['2', '3']:  # 只生成DMG或PKG
            print("注意：DMG和PKG格式需要先生成.app文件")
            if not self.config.utils.ask_yes_no("是否先生成.app文件?", default='y'):
                print("已取消打包")
                return False
        
        # 处理多格式打包
        if self.package_choice in ['5', '6', '7']:
            print("将进行多格式打包，这可能需要较长时间...")
        
        return True
    
    def _handle_linux_pre_build(self):
        """处理Linux平台的构建前逻辑"""
        if self.package_choice in ['2', '3']:  # 只生成DEB或RPM
            print("注意：DEB和RPM格式需要先生成ELF可执行文件")
            if not self.config.utils.ask_yes_no("是否先生成ELF文件?", default='y'):
                print("已取消打包")
                return False
        
        # 处理多格式打包
        if self.package_choice in ['4', '5', '6']:
            print("将进行多格式打包，这可能需要较长时间...")
        
        return True
    
    def handle_post_build(self, app_name, build_path):
        """处理构建后的平台相关逻辑"""
        if not self.package_choice:
            return True
        
        if self.config.current_os == 'Darwin':
            return self._handle_mac_post_build(app_name, build_path)
        elif self.config.current_os == 'Linux':
            return self._handle_linux_post_build(app_name, build_path)
        
        return True
    
    def _handle_mac_post_build(self, app_name, app_path):
        """处理Mac平台的构建后逻辑"""
        from src.constants.config import MAC_PACKAGE_NAME, APP_VERSION
        
        # 更新 Info.plist 中的版本信息
        info_plist_path = os.path.join(app_path, 'Contents', 'Info.plist')
        if os.path.exists(info_plist_path):
            try:
                import plistlib
                with open(info_plist_path, 'rb') as f:
                    plist_data = plistlib.load(f)
                
                # 更新版本信息
                plist_data['CFBundleShortVersionString'] = APP_VERSION
                plist_data['CFBundleVersion'] = APP_VERSION
                
                with open(info_plist_path, 'wb') as f:
                    plistlib.dump(plist_data, f)
                
                print(f"✅ 已更新版本信息为 {APP_VERSION}")
            except Exception as e:
                print(f"⚠️  更新版本信息失败: {e}")
        
        # 修复之前 utils 调用的问题
        from .utils import ask_yes_no
        
        if self.package_choice == '4':
            # Mac App Store 专用处理
            if ask_yes_no("是否创建 Mac App Store 专用包？"):
                if os.path.exists(app_path):
                    create_mac_app_store_package(app_name, app_path, self.config.target_arch, 
                                               MAC_PACKAGE_NAME, APP_VERSION)
        else:
            # 其他格式处理
            if ask_yes_no("是否创建 DMG 安装包？"):
                if os.path.exists(app_path):
                    create_dmg(app_name, app_path, self.config.target_arch)
            
            if ask_yes_no("是否创建 PKG 安装包？"):
                if os.path.exists(app_path):
                    create_pkg(app_name, app_path, self.config.target_arch, 
                              MAC_PACKAGE_NAME, APP_VERSION)
        
        return True
    
    def _handle_linux_post_build(self, app_name, elf_path):
        """处理Linux平台的构建后逻辑"""
        from src.constants.config import APP_VERSION
        
        if self.package_choice in ['2', '4', '6'] and os.path.exists(elf_path):
            print("\n正在生成DEB文件...")
            create_deb(app_name, elf_path, self.config.target_arch, APP_VERSION)
        
        if self.package_choice in ['3', '5', '6'] and os.path.exists(elf_path):
            print("\n正在生成RPM文件...")
            create_rpm(app_name, elf_path, self.config.target_arch, APP_VERSION)
        
        return True
    
    def get_format_description(self):
        """获取当前选择的格式描述"""
        if self.config.current_os == 'Darwin':
            format_names = {
                '1': '.app',
                '2': '.dmg',
                '3': '.pkg',
                '4': 'Mac App Store 专用',
                '5': '.app + .dmg',
                '6': '.app + .pkg',
                '7': '.app + .dmg + .pkg'
            }
        elif self.config.current_os == 'Linux':
            format_names = {
                '1': 'ELF',
                '2': '.deb',
                '3': '.rpm',
                '4': 'ELF + .deb',
                '5': 'ELF + .rpm',
                '6': 'ELF + .deb + .rpm'
            }
        else:
            return "可执行文件"
        
        return format_names.get(self.package_choice, "未知")