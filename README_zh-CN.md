# 矩形马赛克桌面版

<p align="center">
  <strong><a href="./README.md">English</a> | 简体中文</strong>
</p>

<div align="center">
  <img src="assets/icon.png" alt="矩形马赛克桌面版" width="128" height="128">
  <h3>矩形马赛克桌面版</h3>
  <a href="https://apps.microsoft.com/detail/9p28pvb6jq79?referrer=appbadge&mode=direct" target="_blank">
    <img src="https://get.microsoft.com/images/en-us%20dark.svg" alt="从 Microsoft Store 获取" width="200">
  </a>
  <a href="https://apps.apple.com/us/app/rectangular-mosaic-desktop/id6754189038" target="_blank">
    <img src="https://developer.apple.com/app-store/marketing/guidelines/images/badge-download-on-the-mac-app-store.svg" alt="在 Mac App Store 下载">
  </a>
</div>

## 项目简介

本项目是一个基于 PySide6 的图片马赛克工具，支持通过鼠标矩形框选图片区域并一键打马赛克，适合对图片敏感信息进行快速处理。

## 主要功能
- 支持图片上传、显示
- 鼠标拖拽矩形框选区域
- 框选区域一键马赛克处理
- 清除图像功能，重置历史记录
- 支持图片保存
- 界面简洁，操作便捷

## 安装与运行

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 运行主程序

```bash
python main.py
```

## 构建可执行文件

### 交互式构建（推荐）

使用交互式构建脚本：

```bash
python build.py
```

脚本将引导您完成：
- 目标架构选择
- 构建模式选择（onedir/onefile）
- 平台特定打包选项

### 直接 PyInstaller 命令

构建 onedir 版本（生成包含多个文件的文件夹）：

```bash
pyinstaller --onedir --name "RectangularMosaic" --add-data "assets;assets" --add-data "src/localization/translations;src/localization/translations" --icon="assets/icon.ico" --noconsole main.py
```

构建 onefile 版本（生成单个可执行文件）：

```bash
pyinstaller --onefile --name "RectangularMosaic" --add-data "assets;assets" --add-data "src/localization/translations;src/localization/translations" --icon="assets/icon.ico" --noconsole main.py
```

构建完成后，可执行文件将在 `dist/` 目录中。

## 目录结构

```
/src
  /features
    edit_history.py     # 编辑历史管理
    file_manager.py     # 文件操作
    image_loader.py     # 图片加载与保存
    image_mosaic.py     # 马赛克处理逻辑
  /gui
    about_dialog.py     # 关于对话框
    image_viewer.py     # 图像显示组件
    main_window.py      # 主应用程序窗口
    menu_bar.py         # 应用程序菜单栏
    status_bar.py       # 状态栏组件
    theme_manager.py    # UI主题管理
    ui_components.py    # UI组件
    ui_state_manager.py # UI状态管理
  /localization
    translations/       # 多语言翻译文件
    translator.py       # 翻译管理
  /utils
    rect_selector.py    # 框选工具
    selectable_label.py # 可选标签组件
  /constants
    config.py           # 配置常量
main.py                # 启动入口
requirements.txt       # 依赖文件
.gitignore             # Git 忽略文件
README.md              # 项目说明文档
```

## 使用说明

1. 启动程序后，点击"上传图片"选择本地图片。
2. 在图片上用鼠标拖拽框选需要打马赛克的区域。
3. 点击"应用马赛克"按钮，对选中区域进行马赛克处理。
4. 如需清除当前图像并重置所有历史记录，点击"清除图像"按钮。
5. 如需保存处理后的图片，点击"保存图片"按钮。

## 开发规范
- 代码高内聚、低耦合，模块化设计，便于维护和扩展。
- 每个模块、函数、类均有详细中文注释。
- 目录结构清晰，便于查找和管理。

## 依赖环境
- Python 3.7 及以上
- PySide6 6.5.0 及以上

## 贡献与反馈
如有建议或问题，欢迎提交 issue 或 PR。

- **加入QQ群参与讨论：** [彩旗开源交流群](https://qm.qq.com/q/fGavz3UxCo)
- **加入Discord服务器：** [彩旗开源社区](https://discord.gg/thWGWq7CwA)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sihuangtech/rectangular-mosaic-desktop&type=Date)](https://www.star-history.com/#sihuangtech/rectangular-mosaic-desktop&Date)