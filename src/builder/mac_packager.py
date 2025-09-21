"""
Mac平台打包模块
处理Mac平台的.app、.dmg、.pkg打包以及Mac App Store相关功能
"""
import os
import subprocess
import shutil
from .utils import run_command


def create_dmg(app_name, app_path, target_arch):
    """创建DMG磁盘映像文件"""
    try:
        # 添加架构后缀
        arch_suffix = f"-{target_arch}" if target_arch else ""
        dmg_name = f"{app_name}{arch_suffix}.dmg"
        dmg_path = f"dist/{dmg_name}"
        
        # 创建临时目录用于DMG构建
        temp_dir = f"temp_dmg_{app_name.lower().replace(' ', '_')}"
        app_temp_path = f"{temp_dir}/{app_name}.app"
        
        # 复制.app文件到临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        shutil.copytree(app_path, app_temp_path)
        
        # 创建Applications快捷方式
        apps_link = f"{temp_dir}/Applications"
        if not os.path.exists(apps_link):
            os.symlink("/Applications", apps_link)
        
        # 使用hdiutil创建DMG
        cmd = [
            'hdiutil', 'create', '-volname', app_name,
            '-srcfolder', temp_dir, '-ov', '-format', 'UDZO',
            dmg_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        if result.returncode == 0:
            print(f"✅ DMG文件创建成功：{dmg_path}")
        else:
            print(f"❌ DMG创建失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 创建DMG时出错：{e}")


def create_pkg(app_name, app_path, target_arch, mac_package_name, app_version):
    """创建PKG安装包文件"""
    try:
        # 添加架构后缀
        arch_suffix = f"-{target_arch}" if target_arch else ""
        pkg_name = f"{app_name}{arch_suffix}.pkg"
        pkg_path = f"dist/{pkg_name}"
        
        # 使用指定的Mac包名
        bundle_id = mac_package_name
        
        # 使用pkgbuild创建PKG
        cmd = [
            'pkgbuild', '--component', app_path,
            '--install-location', '/Applications',
            '--identifier', bundle_id,
            '--version', app_version, pkg_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PKG文件创建成功：{pkg_path}")
        else:
            print(f"❌ PKG创建失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 创建PKG时出错：{e}")


def create_mac_app_store_package(app_name, app_path, target_arch, mac_package_name, app_version):
    """创建Mac App Store专用包（需要额外签名和配置）"""
    print("\n⚠️  Mac App Store 打包说明：")
    print("1. 需要有效的 Apple Developer 账号和 App Store 证书")
    print("2. 需要在 Xcode 中配置 App ID 和 Provisioning Profile")
    print("3. 需要进行代码签名和 Notarization")
    print("4. 需要通过 Apple 的 App Review 审核")
    print()
    
    # 生成 entitlements 文件（Mac App Store 必需）
    entitlements_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.print</key>
    <true/>
</dict>
</plist>"""
    
    entitlements_path = "dist/mac_app_store.entitlements"
    os.makedirs("dist", exist_ok=True)
    with open(entitlements_path, 'w') as f:
        f.write(entitlements_content)
    
    print(f"✅ 已生成 entitlements 文件：{entitlements_path}")
    print("\n📋 后续步骤：")
    print("1. 在 Apple Developer Portal 创建 App ID：", mac_package_name)
    print("2. 在 Xcode 中配置签名证书和 Provisioning Profile")
    print("3. 使用 codesign 命令对 .app 进行签名：")
    print(f"   codesign --deep --force --verify --verbose --sign 'Developer ID Application: Your Name' --entitlements {entitlements_path} {app_path}")
    print("4. 使用 productbuild 创建安装包：")
    print(f"   productbuild --component {app_path} /Applications --sign 'Developer ID Installer: Your Name' --product dist/{app_name}.pkg")
    print("5. 使用 notarytool 进行 Notarization")
    print("6. 通过 Xcode 或 Application Loader 上传到 App Store Connect")
    print("\n⚠️  注意：上传到 Mac App Store 需要满足 Apple 的所有审核要求，包括：")
    print("- 应用必须符合 App Store Review Guidelines")
    print("- 必须启用 App Sandbox")
    print("- 必须支持 Apple 的所有技术要求")
    print("- 需要通过 Apple 的审核流程")


def get_mac_package_format():
    """获取Mac平台的打包格式选择"""
    print("\n=== Mac 打包格式选择 ===")
    print("1. .app 应用包 (默认)")
    print("2. .dmg 磁盘映像")
    print("3. .pkg 安装包")
    print("4. Mac App Store 专用 (.app + 签名配置)")
    print("5. 同时生成 .app 和 .dmg")
    print("6. 同时生成 .app 和 .pkg")
    print("7. 同时生成所有格式 (.app + .dmg + .pkg)")
    print("输入 'q' 或 'quit' 退出打包")
    
    while True:
        choice = input("请选择打包格式 (1-7, 默认1): ").strip().lower()
        if choice in ['q', 'quit']:
            return None
        if not choice:
            choice = '1'
        
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            return choice
        else:
            print("无效选择，请输入 1-7")