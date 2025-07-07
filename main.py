# -*- coding: utf-8 -*-
"""
主程序入口

用途：
    启动 PySide6 应用，加载主界面 MosaicTool。

使用场景：
    直接运行 main.py 启动图片马赛克工具。
"""
import sys
from PySide6.QtWidgets import QApplication
# 导入主界面类
from src.features.mosaic_tool import MosaicTool

def main():
    """
    应用程序主入口，初始化并启动主窗口。
    """
    app = QApplication(sys.argv)
    window = MosaicTool()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 