# -*- coding: utf-8 -*-
"""
主程序入口

用途：
    启动 PySide6 应用，加载主界面 MosaicTool。

使用场景：
    直接运行 main.py 启动图片马赛克工具。
"""
import sys
import json
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
from src.gui.main_window import MainWindow
from src.constants.config import APP_NAME, ORGANIZATION_NAME, APP_VERSION, DEFAULT_LANGUAGE, LANGUAGE_CONFIG_FILE
from src.localization import set_language, tr

def load_language_config():
    """加载语言配置文件"""
    try:
        if os.path.exists(LANGUAGE_CONFIG_FILE):
            with open(LANGUAGE_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', DEFAULT_LANGUAGE)
    except Exception:
        pass
    return DEFAULT_LANGUAGE

def save_language_config(language_code):
    """保存语言配置"""
    try:
        config = {'language': language_code}
        with open(LANGUAGE_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def main():
    """
    应用程序主入口，初始化并启动主窗口。
    """
    app = QApplication(sys.argv)
    
    # 初始化本地化系统
    saved_language = load_language_config()
    set_language(saved_language)
    
    # 设置应用元数据（使用翻译后的名称）
    QCoreApplication.setApplicationName(tr('app_name', APP_NAME))
    QCoreApplication.setOrganizationName(tr('organization_name', ORGANIZATION_NAME))
    QCoreApplication.setApplicationVersion(APP_VERSION)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()