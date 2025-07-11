# 图片马赛克工具

## 项目简介

本项目是一个基于 PySide6 的图片马赛克工具，支持通过鼠标矩形框选图片区域并一键打马赛克，适合对图片敏感信息进行快速处理。

## 主要功能
- 支持图片上传、显示
- 鼠标拖拽矩形框选区域
- 框选区域一键马赛克处理
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

## 目录结构

```
/src
  /features
    mosaic_tool.py      # 主界面与功能入口
    image_mosaic.py     # 马赛克处理逻辑
    image_loader.py     # 图片加载与保存
  /utils
    rect_selector.py    # 框选工具
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
3. 点击"区域马赛克"按钮，对选中区域进行马赛克处理。
4. 如需保存处理后的图片，点击"保存图片"按钮。

## 开发规范
- 代码高内聚、低耦合，模块化设计，便于维护和扩展。
- 每个模块、函数、类均有详细中文注释。
- 目录结构清晰，便于查找和管理。

## 依赖环境
- Python 3.7 及以上
- PySide6 6.5.0 及以上

## 贡献与反馈
如有建议或问题，欢迎提交 issue 或 PR。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Snake-Konginchrist/rectangular-mosaic&type=Date)](https://www.star-history.com/#Snake-Konginchrist/rectangular-mosaic&Date) 