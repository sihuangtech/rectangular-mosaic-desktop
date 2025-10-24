# -*- coding: utf-8 -*-
"""
主题管理器模块 - 管理应用程序的主题设置
"""
from PySide6.QtCore import QObject, Signal, QSettings
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication
from src.localization import tr
from typing import Dict


class ThemeManager(QObject):
    """主题管理器 - 管理应用程序的主题设置"""
    
    # 主题模式常量
    THEME_SYSTEM = "system"
    THEME_LIGHT = "light"
    THEME_DARK = "dark"
    
    # 信号
    theme_changed = Signal(str)  # 主题改变信号，参数为新主题模式
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("RectangularMosaic", "ThemeSettings")
        self.current_theme = self.load_theme()
        self.system_theme = self.detect_system_theme()
        
        # 主题配色方案
        self.light_palette = self.create_light_palette()
        self.dark_palette = self.create_dark_palette()
    
    def get_available_themes(self) -> Dict[str, str]:
        """获取可用的主题列表"""
        return {
            self.THEME_SYSTEM: tr("theme_system", "Follow System"),
            self.THEME_LIGHT: tr("theme_light", "Light"),
            self.THEME_DARK: tr("theme_dark", "Dark")
        }
    
    def get_current_theme(self) -> str:
        """获取当前主题模式"""
        return self.current_theme
    
    def set_theme(self, theme: str) -> bool:
        """设置主题模式"""
        if theme not in [self.THEME_SYSTEM, self.THEME_LIGHT, self.THEME_DARK]:
            return False
        
        self.current_theme = theme
        self.apply_theme()
        self.save_theme()
        self.theme_changed.emit(theme)
        return True
    
    def apply_theme(self):
        """应用当前主题"""
        app = QApplication.instance()
        if not app:
            return
        
        if self.current_theme == self.THEME_SYSTEM:
            # 跟随系统主题
            effective_theme = self.system_theme
        else:
            effective_theme = self.current_theme
        
        if effective_theme == self.THEME_DARK:
            self.apply_dark_theme(app)
        else:
            self.apply_light_theme(app)
    
    def apply_light_theme(self, app: QApplication):
        """应用浅色主题"""
        app.setStyle("Fusion")
        app.setPalette(self.light_palette)
        
        # 设置样式表
        light_stylesheet = self.get_light_stylesheet()
        app.setStyleSheet(light_stylesheet)
    
    def apply_dark_theme(self, app: QApplication):
        """应用深色主题"""
        app.setStyle("Fusion")
        app.setPalette(self.dark_palette)
        
        # 设置样式表
        dark_stylesheet = self.get_dark_stylesheet()
        app.setStyleSheet(dark_stylesheet)
    
    def create_light_palette(self) -> QPalette:
        """创建浅色主题调色板"""
        palette = QPalette()
        
        # 基础颜色
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(0, 120, 215))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette
    
    def create_dark_palette(self) -> QPalette:
        """创建深色主题调色板"""
        palette = QPalette()
        
        # 基础颜色
        palette.setColor(QPalette.Window, QColor(45, 45, 48))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
        palette.setColor(QPalette.ToolTipBase, QColor(45, 45, 48))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(62, 62, 66))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(0, 150, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 150, 255))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette
    
    def get_light_stylesheet(self) -> str:
        """获取浅色主题样式表"""
        return """
        QPushButton {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 6px 12px;
            background-color: #ffffff;
            color: #333333;
        }
        
        QPushButton:hover {
            background-color: #f0f0f0;
            border-color: #999999;
        }
        
        QPushButton:pressed {
            background-color: #e0e0e0;
            border-color: #666666;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 4px;
            background-color: #ffffff;
            color: #333333;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border-color: #0078d4;
            outline: none;
        }
        
        QMenuBar {
            background-color: #f0f0f0;
            border-bottom: 1px solid #cccccc;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 1px solid #cccccc;
        }
        
        QMenu::item {
            padding: 4px 20px;
        }
        
        QMenu::item:selected {
            background-color: #e0e0e0;
        }
        """
    
    def get_dark_stylesheet(self) -> str:
        """获取深色主题样式表"""
        return """
        QPushButton {
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 6px 12px;
            background-color: #3e3e42;
            color: #ffffff;
        }
        
        QPushButton:hover {
            background-color: #4a4a4e;
            border-color: #777777;
        }
        
        QPushButton:pressed {
            background-color: #2d2d30;
            border-color: #999999;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px;
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border-color: #0096ff;
            outline: none;
        }
        
        QMenuBar {
            background-color: #2d2d30;
            border-bottom: 1px solid #555555;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
            color: #ffffff;
        }
        
        QMenuBar::item:selected {
            background-color: #3e3e42;
        }
        
        QMenu {
            background-color: #2d2d30;
            border: 1px solid #555555;
            color: #ffffff;
        }
        
        QMenu::item {
            padding: 4px 20px;
        }
        
        QMenu::item:selected {
            background-color: #3e3e42;
        }
        """
    
    def detect_system_theme(self) -> str:
        """检测系统主题"""
        try:
            # Windows 系统主题检测
            import winreg
            
            # 尝试读取 Windows 注册表中的系统主题设置
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            
            return self.THEME_LIGHT if value else self.THEME_DARK
        except Exception:
            # 如果检测失败，默认返回浅色主题
            return self.THEME_LIGHT
    
    def save_theme(self):
        """保存主题设置"""
        self.settings.setValue("theme", self.current_theme)
    
    def load_theme(self) -> str:
        """加载主题设置"""
        saved_theme = self.settings.value("theme", self.THEME_SYSTEM)
        if saved_theme in [self.THEME_SYSTEM, self.THEME_LIGHT, self.THEME_DARK]:
            return saved_theme
        return self.THEME_SYSTEM
    
    def get_theme_display_name(self, theme: str) -> str:
        """获取主题的显示名称"""
        themes = self.get_available_themes()
        return themes.get(theme, theme)


# 全局主题管理器实例
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """获取全局主题管理器实例"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager