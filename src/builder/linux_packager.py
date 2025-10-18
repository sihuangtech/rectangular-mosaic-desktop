"""
Linux平台打包模块
处理Linux平台的.deb和.rpm打包
"""
import os
import subprocess
import shutil
from .utils import run_command


def create_deb(app_name, elf_path, target_arch, app_version="1.0"):
    """创建DEB安装包文件"""
    try:
        # 根据架构确定包名
        if target_arch == 'x86_64':
            arch_name = 'amd64'
        elif target_arch == 'arm64':
            arch_name = 'arm64'
        else:
            arch_name = target_arch or 'amd64'
        
        deb_name = f"{app_name.lower().replace(' ', '-')}_{app_version}_{arch_name}.deb"
        deb_path = f"dist/{deb_name}"
        
        # 创建临时目录结构
        temp_dir = f"temp_deb_{app_name.lower().replace(' ', '_')}"
        os.makedirs(f"{temp_dir}/DEBIAN", exist_ok=True)
        os.makedirs(f"{temp_dir}/usr/local/bin", exist_ok=True)
        os.makedirs(f"{temp_dir}/usr/share/applications", exist_ok=True)
        os.makedirs(f"{temp_dir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
        
        # 复制可执行文件
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
        icon_src = "assets/icon.png"
        if os.path.exists(icon_src):
            shutil.copy2(icon_src, f"{temp_dir}/usr/share/icons/hicolor/256x256/apps/{app_name.lower().replace(' ', '-')}.png")
        
        # 创建control文件
        control_content = f"""Package: {app_name.lower().replace(' ', '-')}
Version: {app_version}
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


def create_rpm(app_name, elf_path, target_arch, app_version="1.0"):
    """创建RPM安装包文件"""
    try:
        # 根据架构确定包名
        if target_arch == 'x86_64':
            arch_name = 'x86_64'
        elif target_arch == 'arm64':
            arch_name = 'aarch64'
        else:
            arch_name = target_arch or 'x86_64'
        
        rpm_name = f"{app_name.lower().replace(' ', '-')}-{app_version}-1.{arch_name}.rpm"
        rpm_path = f"dist/{rpm_name}"
        
        # 创建临时目录结构
        temp_dir = f"temp_rpm_{app_name.lower().replace(' ', '_')}"
        os.makedirs(f"{temp_dir}/BUILD", exist_ok=True)
        os.makedirs(f"{temp_dir}/RPMS", exist_ok=True)
        os.makedirs(f"{temp_dir}/SOURCES", exist_ok=True)
        os.makedirs(f"{temp_dir}/SPECS", exist_ok=True)
        
        # 复制可执行文件到BUILD目录
        build_bin_dir = f"{temp_dir}/BUILD/usr/local/bin"
        os.makedirs(build_bin_dir, exist_ok=True)
        shutil.copy2(elf_path, f"{build_bin_dir}/{app_name.lower().replace(' ', '-')}")
        
        # 创建spec文件
        spec_content = f"""Name: {app_name.lower().replace(' ', '-')}
Version: {app_version}
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


def get_linux_package_format():
    """获取Linux平台的打包格式选择"""
    print("\n=== Linux 打包格式选择 ===")
    print("1. ELF 可执行文件 (默认)")
    print("2. DEB 安装包 (Debian/Ubuntu)")
    print("3. RPM 安装包 (RedHat/CentOS)")
    print("4. 同时生成 ELF 和 DEB")
    print("5. 同时生成 ELF 和 RPM")
    print("6. 同时生成所有格式 (ELF + DEB + RPM)")
    print("输入 'q' 或 'quit' 退出打包")
    
    while True:
        choice = input("请选择打包格式 (1-6, 默认1): ").strip().lower()
        if choice in ['q', 'quit']:
            return None
        if not choice:
            choice = '1'
        
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        else:
            print("无效选择，请输入 1-6")