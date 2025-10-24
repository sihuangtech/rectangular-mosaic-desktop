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
    
    def retranslate_ui(self):
        """重新翻译UI文本"""
        # 只更新当前状态，不重置状态
        current_status = self.status_label.text()
        
        # 定义状态消息的翻译映射
        status_translations = {
            tr("ready", "Ready"): tr("ready", "Ready"),
            tr("image_loaded", "Image loaded - Undo/Redo available"): tr("image_loaded", "Image loaded - Undo/Redo available"),
            tr("image_loaded_undo", "Image loaded - Undo available"): tr("image_loaded_undo", "Image loaded - Undo available"),
            tr("image_loaded_redo", "Image loaded - Redo available"): tr("image_loaded_redo", "Image loaded - Redo available"),
            tr("image_loaded_only", "Image loaded"): tr("image_loaded_only", "Image loaded"),
            tr("mosaic_applied", "Mosaic applied"): tr("mosaic_applied", "Mosaic applied"),
        }
        
        # 如果当前状态在翻译映射中，则更新为新的翻译
        for original, translation in status_translations.items():
            if current_status == original:
                self.status_label.setText(translation)
                break
    
    def show_message(self, message, timeout=0):
        """显示状态消息"""
        self.status_label.setText(message)
        if timeout > 0:
            # 如果需要自动清除，可以使用QTimer
            pass
    
    def show_image_loaded(self):
        """显示图片加载完成的消息"""
        self.show_message(tr("image_loaded", "Image loaded - Undo/Redo available"))
    
    def show_mosaic_applied(self):
        """显示马赛克应用完成的消息"""
        self.show_message(tr("mosaic_applied", "Mosaic applied"))
    
    def show_error(self, error_message):
        """显示错误消息"""
        self.show_message(tr("error", f"Error: {error_message}"))
    
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
                self.show_message(tr("image_loaded", "Image loaded - Undo/Redo available"))
            elif can_undo:
                self.show_message(tr("image_loaded_undo", "Image loaded - Undo available"))
            elif can_redo:
                self.show_message(tr("image_loaded_redo", "Image loaded - Redo available"))
            else:
                self.show_message(tr("image_loaded_only", "Image loaded"))
        else:
            self.show_message(tr("ready", "Ready"))
            self.clear_image_info()