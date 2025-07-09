# -*- coding: utf-8 -*-
"""
交互式参数选择 + 自动平台检测 PyInstaller 打包脚本

用途：
    自动检测当前操作系统，打包参数由用户运行时选择。
    支持指定目标架构（x86_64/arm64），可跨架构打包。

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

def get_mac_package_format():
    """获取Mac平台的打包格式选择"""
    print("\n=== Mac 打包格式选择 ===")
    print("1. .app 应用包 (默认)")
    print("2. .dmg 磁盘映像")
    print("3. .pkg 安装包")
    print("4. 同时生成 .app 和 .dmg")
    print("5. 同时生成 .app 和 .pkg")
    print("6. 同时生成所有格式 (.app + .dmg + .pkg)")
    
    while True:
        choice = input("请选择打包格式 (1-6, 默认1): ").strip()
        if not choice:
            choice = '1'
        
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        else:
            print("无效选择，请输入 1-6")

def get_linux_package_format():
    """获取Linux平台的打包格式选择"""
    print("\n=== Linux 打包格式选择 ===")
    print("1. ELF 可执行文件 (默认)")
    print("2. .deb 安装包 (Debian/Ubuntu)")
    print("3. .rpm 安装包 (RedHat/CentOS/Fedora)")
    print("4. 同时生成 ELF 和 .deb")
    print("5. 同时生成 ELF 和 .rpm")
    print("6. 同时生成所有格式 (ELF + .deb + .rpm)")
    
    while True:
        choice = input("请选择打包格式 (1-6, 默认1): ").strip()
        if not choice:
            choice = '1'
        
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        else:
            print("无效选择，请输入 1-6")

def get_architecture_choice():
    """获取用户选择的架构"""
    print("\n=== 架构选择 ===")
    print("1. x86_64 (Intel/AMD 64位)")
    print("2. arm64 (Apple Silicon/ARM 64位)")
    print("3. 自动检测当前系统架构")
    
    while True:
        choice = input("请选择目标架构 (1/2/3, 默认3): ").strip()
        if not choice:
            choice = '3'
        
        if choice == '1':
            return 'x86_64'
        elif choice == '2':
            return 'arm64'
        elif choice == '3':
            return 'auto'
        else:
            print("无效选择，请输入 1、2 或 3")

def detect_current_arch():
    """检测当前系统架构"""
    machine = platform.machine().lower()
    if machine in ['x86_64', 'amd64']:
        return 'x86_64'
    elif machine in ['arm64', 'aarch64']:
        return 'arm64'
    else:
        return machine

def create_dmg(app_name, app_path, target_arch):
    """创建DMG磁盘映像文件"""
    try:
        # 添加架构后缀
        arch_suffix = f"-{target_arch}" if target_arch else ""
        dmg_name = f"{app_name}{arch_suffix}.dmg"
        dmg_path = f"dist/{dmg_name}"
        
        # 使用hdiutil创建DMG
        cmd = [
            'hdiutil', 'create', '-volname', f"{app_name}{arch_suffix}",
            '-srcfolder', app_path, '-ov', '-format', 'UDZO', dmg_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ DMG文件创建成功：{dmg_path}")
        else:
            print(f"❌ DMG创建失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 创建DMG时出错：{e}")

def create_pkg(app_name, app_path, target_arch):
    """创建PKG安装包文件"""
    try:
        # 添加架构后缀
        arch_suffix = f"-{target_arch}" if target_arch else ""
        pkg_name = f"{app_name}{arch_suffix}.pkg"
        pkg_path = f"dist/{pkg_name}"
        
        # 使用pkgbuild创建PKG
        cmd = [
            'pkgbuild', '--component', app_path,
            '--install-location', '/Applications',
            '--identifier', f'com.mosaic.{app_name.lower().replace(" ", "")}{arch_suffix}',
            '--version', '1.0', pkg_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PKG文件创建成功：{pkg_path}")
        else:
            print(f"❌ PKG创建失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 创建PKG时出错：{e}")

def create_deb(app_name, elf_path, target_arch):
    """创建DEB安装包文件"""
    try:
        # 根据架构确定包名
        if target_arch == 'x86_64':
            arch_name = 'amd64'
        elif target_arch == 'arm64':
            arch_name = 'arm64'
        else:
            arch_name = target_arch or 'amd64'
        
        deb_name = f"{app_name.lower().replace(' ', '-')}_1.0_{arch_name}.deb"
        deb_path = f"dist/{deb_name}"
        
        # 创建临时目录结构
        temp_dir = f"temp_deb_{app_name.lower().replace(' ', '_')}"
        os.makedirs(f"{temp_dir}/DEBIAN", exist_ok=True)
        os.makedirs(f"{temp_dir}/usr/local/bin", exist_ok=True)
        os.makedirs(f"{temp_dir}/usr/share/applications", exist_ok=True)
        os.makedirs(f"{temp_dir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
        
        # 复制可执行文件
        import shutil
        shutil.copy2(elf_path, f"{temp_dir}/usr/local/bin/{app_name.lower().replace(' ', '-')}")
        
        # 创建桌面文件
        desktop_content = f"""[Desktop Entry]
Name={app_name}
Comment=图片马赛克处理工具
Exec={app_name.lower().replace(' ', '-')}
Icon={app_name.lower().replace(' ', '-')}
Terminal=false
Type=Application
Categories=Graphics;
"""
        with open(f"{temp_dir}/usr/share/applications/{app_name.lower().replace(' ', '-')}.desktop", 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # 复制图标
        icon_src = "assets/icons/app.png"
        if os.path.exists(icon_src):
            shutil.copy2(icon_src, f"{temp_dir}/usr/share/icons/hicolor/256x256/apps/{app_name.lower().replace(' ', '-')}.png")
        
        # 创建control文件
        control_content = f"""Package: {app_name.lower().replace(' ', '-')}
Version: 1.0
Architecture: {arch_name}
Maintainer: Mosaic Tool Developer
Description: 图片马赛克处理工具
 一个用于对图片进行马赛克处理的图形界面工具
"""
        with open(f"{temp_dir}/DEBIAN/control", 'w', encoding='utf-8') as f:
            f.write(control_content)
        
        # 使用dpkg-deb创建DEB包
        cmd = ['dpkg-deb', '--build', temp_dir, deb_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        if result.returncode == 0:
            print(f"✅ DEB文件创建成功：{deb_path}")
        else:
            print(f"❌ DEB创建失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 创建DEB时出错：{e}")

def create_rpm(app_name, elf_path, target_arch):
    """创建RPM安装包文件"""
    try:
        # 根据架构确定包名
        if target_arch == 'x86_64':
            arch_name = 'x86_64'
        elif target_arch == 'arm64':
            arch_name = 'aarch64'
        else:
            arch_name = target_arch or 'x86_64'
        
        rpm_name = f"{app_name.lower().replace(' ', '-')}-1.0-1.{arch_name}.rpm"
        rpm_path = f"dist/{rpm_name}"
        
        # 创建临时目录结构
        temp_dir = f"temp_rpm_{app_name.lower().replace(' ', '_')}"
        os.makedirs(f"{temp_dir}/BUILD", exist_ok=True)
        os.makedirs(f"{temp_dir}/RPMS", exist_ok=True)
        os.makedirs(f"{temp_dir}/SOURCES", exist_ok=True)
        os.makedirs(f"{temp_dir}/SPECS", exist_ok=True)
        
        # 复制可执行文件到BUILD目录
        import shutil
        build_bin_dir = f"{temp_dir}/BUILD/usr/local/bin"
        os.makedirs(build_bin_dir, exist_ok=True)
        shutil.copy2(elf_path, f"{build_bin_dir}/{app_name.lower().replace(' ', '-')}")
        
        # 创建spec文件
        spec_content = f"""Name: {app_name.lower().replace(' ', '-')}
Version: 1.0
Release: 1
Summary: 图片马赛克处理工具
License: LGPL-3.0
URL: https://gitee.com/Snake-Konginchrist/rectangular-batch-mosaic
BuildArch: {arch_name}

%description
一个用于对图片进行马赛克处理的图形界面工具

%files
%defattr(-,root,root,-)
/usr/local/bin/{app_name.lower().replace(' ', '-')}

%post
chmod +x /usr/local/bin/{app_name.lower().replace(' ', '-')}

%clean
rm -rf $RPM_BUILD_ROOT
"""
        spec_file = f"{temp_dir}/SPECS/{app_name.lower().replace(' ', '-')}.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        # 使用rpmbuild创建RPM包
        cmd = ['rpmbuild', '--define', f'_topdir {os.path.abspath(temp_dir)}', '-bb', spec_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 移动生成的RPM文件
        if result.returncode == 0:
            generated_rpm = f"{temp_dir}/RPMS/{arch_name}/{rpm_name}"
            if os.path.exists(generated_rpm):
                shutil.move(generated_rpm, rpm_path)
                print(f"✅ RPM文件创建成功：{rpm_path}")
            else:
                print(f"❌ RPM文件未找到：{generated_rpm}")
        else:
            print(f"❌ RPM创建失败：{result.stderr}")
        
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"❌ 创建RPM时出错：{e}")

def main():
    current_os = platform.system()
    current_arch = detect_current_arch()
    
    print(f'检测到当前平台：{current_os} ({current_arch})')
    
    if current_os == 'Windows':
        print('将打包为 .exe 可执行文件')
        default_icon = 'assets/icons/app.ico'
        default_name = '图片马赛克工具'
        mac_package_choice = None
        linux_package_choice = None
    elif current_os == 'Darwin':
        print('Mac平台支持多种打包格式')
        default_icon = 'assets/icons/app.icns'
        default_name = '图片马赛克工具'
        mac_package_choice = get_mac_package_format()
        linux_package_choice = None
    elif current_os == 'Linux':
        print('Linux平台支持多种打包格式')
        default_icon = 'assets/icons/app.png'
        default_name = '图片马赛克工具'
        mac_package_choice = None
        linux_package_choice = get_linux_package_format()
    else:
        print(f'不支持的操作系统：{current_os}，已退出。')
        return

    # 架构选择
    target_arch = get_architecture_choice()
    if target_arch == 'auto':
        target_arch = current_arch
        print(f'使用当前系统架构：{target_arch}')
    else:
        print(f'目标架构：{target_arch}')
        
        # 检查跨架构打包的可行性
        if target_arch != current_arch:
            print(f'⚠️  警告：您正在尝试跨架构打包 ({current_arch} -> {target_arch})')
            print('这可能需要额外的工具链支持：')
            if current_os == 'Darwin' and current_arch == 'x86_64' and target_arch == 'arm64':
                print('- 需要安装 Rosetta 2')
                print('- 可能需要使用 conda 或特定 Python 环境')
            elif current_os == 'Darwin' and current_arch == 'arm64' and target_arch == 'x86_64':
                print('- 需要安装 Rosetta 2')
                print('- 可能需要使用 conda 或特定 Python 环境')
            
            if not ask_yes_no("是否继续跨架构打包?", default='n'):
                print("已取消打包")
                return

    # 根据平台打包选择处理
    if current_os == 'Darwin' and mac_package_choice:
        if mac_package_choice in ['2', '3']:  # 只生成DMG或PKG
            print("注意：DMG和PKG格式需要先生成.app文件")
            if not ask_yes_no("是否先生成.app文件?", default='y'):
                print("已取消打包")
                return
        
        # 处理多格式打包
        if mac_package_choice in ['4', '5', '6']:
            print("将进行多格式打包，这可能需要较长时间...")
    
    elif current_os == 'Linux' and linux_package_choice:
        if linux_package_choice in ['2', '3']:  # 只生成DEB或RPM
            print("注意：DEB和RPM格式需要先生成ELF可执行文件")
            if not ask_yes_no("是否先生成ELF文件?", default='y'):
                print("已取消打包")
                return
        
        # 处理多格式打包
        if linux_package_choice in ['4', '5', '6']:
            print("将进行多格式打包，这可能需要较长时间...")
    
    args = ['pyinstaller']

    # 添加架构指定参数
    if target_arch == 'x86_64':
        args += ['--target-arch', 'x86_64']
    elif target_arch == 'arm64':
        args += ['--target-arch', 'arm64']

    # 自动集成 assets/icons 资源目录
    icons_dir = 'assets/icons'
    if os.path.exists(icons_dir):
        sep = ';' if current_os == 'Windows' else ':'
        args += ['--add-data', f'{icons_dir}{sep}{icons_dir}']

    # 自动集成 --name 参数，允许用户自定义
    use_default_name = ask_yes_no(f"是否使用默认应用名 [{default_name}] (--name)?", default='y')
    if use_default_name:
        final_name = default_name
    else:
        custom_name = input("请输入应用名（英文或中文均可）: ").strip()
        final_name = custom_name if custom_name else default_name
    
    # 为Windows添加架构后缀
    if current_os == 'Windows' and target_arch and target_arch != 'auto':
        arch_suffix = f"-{target_arch}"
        final_name_with_arch = f"{final_name}{arch_suffix}"
        args += ['--name', final_name_with_arch]
    else:
        args += ['--name', final_name]

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

    print('\n=== 打包配置 ===')
    print(f'目标平台：{current_os}')
    print(f'目标架构：{target_arch}')
    if current_os == 'Darwin' and mac_package_choice:
        format_names = {
            '1': '.app',
            '2': '.dmg',
            '3': '.pkg',
            '4': '.app + .dmg',
            '5': '.app + .pkg',
            '6': '.app + .dmg + .pkg'
        }
        print(f'打包格式：{format_names.get(mac_package_choice, "未知")}')
    elif current_os == 'Linux' and linux_package_choice:
        format_names = {
            '1': 'ELF',
            '2': '.deb',
            '3': '.rpm',
            '4': 'ELF + .deb',
            '5': 'ELF + .rpm',
            '6': 'ELF + .deb + .rpm'
        }
        print(f'打包格式：{format_names.get(linux_package_choice, "未知")}')
    print('运行命令：', ' '.join(args))
    
    if ask_yes_no("确认开始打包?", default='y'):
        # 执行PyInstaller打包
        subprocess.run(args)
        
        # Mac平台额外处理
        if current_os == 'Darwin' and mac_package_choice:
            app_name = final_name
            app_path = f'dist/{app_name}.app'
            
            if mac_package_choice in ['2', '4', '6'] and os.path.exists(app_path):
                print("\n正在生成DMG文件...")
                create_dmg(app_name, app_path, target_arch)
            
            if mac_package_choice in ['3', '5', '6'] and os.path.exists(app_path):
                print("\n正在生成PKG文件...")
                create_pkg(app_name, app_path, target_arch)
        
        # Linux平台额外处理
        elif current_os == 'Linux' and linux_package_choice:
            app_name = final_name
            elf_path = f'dist/{app_name}'
            
            if linux_package_choice in ['2', '4', '6'] and os.path.exists(elf_path):
                print("\n正在生成DEB文件...")
                create_deb(app_name, elf_path, target_arch)
            
            if linux_package_choice in ['3', '5', '6'] and os.path.exists(elf_path):
                print("\n正在生成RPM文件...")
                create_rpm(app_name, elf_path, target_arch)
        
        print('\n打包完成！可执行文件在 dist 目录下。')
        print(f'生成的文件适用于 {current_os} ({target_arch}) 平台')
    else:
        print("已取消打包")

if __name__ == "__main__":
    main() 