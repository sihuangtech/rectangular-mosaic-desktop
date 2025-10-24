# -*- coding: utf-8 -*-
"""
状态栏组件模块 - 包含应用程序的状态栏
"""
from PySide6.QtWidgets import QStatusBar, QLabel
from src.localization import tr


class AppStatusBar(QStatusBar):
    """应用程序状态栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化状态栏UI"""
        # 左侧状态标签
        self.status_label = QLabel(tr("ready", "Ready"))
        self.addWidget(self.status_label)
        
        # 右侧永久标签
        self.info_label = QLabel("")
        self.addPermanentWidget(self.info_label)
        
        # 设置初始状态
        self.show_message(tr("ready", "Ready"))
    
    def show_message(self, message, timeout=0):
        """显示状态消息"""
        self.status_label.setText(message)
        if timeout > 0:
            # 如果需要自动清除，可以使用定时器
            pass
    
    def show_image_info(self, width, height):
        """显示图片信息"""
        self.info_label.setText(f"{width} × {height}")
    
    def clear_image_info(self):
        """清除图片信息"""
        self.info_label.setText("")
    
    def update_status(self, has_image=False, can_undo=False, can_redo=False):
        """更新状态信息"""
        if has_image:
            if can_undo and can_redo:
                self.show_message("Image loaded - Undo/Redo available")
            elif can_undo:
                self.show_message("Image loaded - Undo available")
            elif can_redo:
                self.show_message("Image loaded - Redo available")
            else:
                self.show_message("Image loaded")
        else:
            self.show_message(tr("ready", "Ready"))
            self.clear_image_info()