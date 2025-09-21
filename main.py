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
from PySide6.QtCore import QCoreApplication
# 导入主界面类和配置
from src.features.mosaic_tool import MosaicTool
from src.constants.config import APP_NAME, ORGANIZATION_NAME, APP_VERSION

def main():
    """
    应用程序主入口，初始化并启动主窗口。
    """
    app = QApplication(sys.argv)
    
    # 设置应用元数据
    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setApplicationVersion(APP_VERSION)
    
    window = MosaicTool()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()