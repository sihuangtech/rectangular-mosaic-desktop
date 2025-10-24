# -*- coding: utf-8 -*-
"""
关于对话框模块 - 显示应用程序信息
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QIcon, QDesktopServices
from src.localization import tr
from src.constants.config import APP_VERSION_DISPLAY
import os


class AboutDialog(QDialog):
    """关于对话框类 (macOS风格)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.set_fixed_size()
    
    def init_ui(self):
        """初始化UI (macOS风格 - 图标在左，内容在右)"""
        self.setWindowTitle("")  # macOS标准关于窗口通常没有标题
        self.setModal(True)
        
        # 主布局 - 水平布局：图标在左，内容在右
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)  # 图标和内容之间的间距
        main_layout.setContentsMargins(30, 20, 30, 20)  # macOS风格边距
        
        # 左侧 - 应用图标
        icon_label = QLabel()
        icon_label.setFixedSize(64, 64)
        
        # 尝试加载应用图标
        icon_paths = [
            os.path.join('assets', 'icon.png'),
            os.path.join('assets', 'icon.ico'),
            ':/icons/app-icon'  # Qt资源路径
        ]
        
        icon_loaded = False
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    icon_loaded = True
                    break
        
        if not icon_loaded:
            icon_label.setText("📷")
            icon_label.setStyleSheet("font-size: 48px; color: #666;")
        
        main_layout.addWidget(icon_label, 0, Qt.AlignTop)  # 图标顶部对齐
        
        # 右侧 - 内容区域
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)  # 内容项之间的紧凑间距
        
        # 应用名称 - macOS风格字体
        app_name_label = QLabel(tr('app_name', 'Rectangular Mosaic'))
        app_name_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #333333;
        """)
        content_layout.addWidget(app_name_label)
        
        # 版本信息 - 包含构建版本
        version_label = QLabel(f"{tr('version', 'Version')} {APP_VERSION_DISPLAY}(1)")  # 简化构建版本
        version_label.setStyleSheet("""
            font-size: 11px;
            color: #666666;
        """)
        content_layout.addWidget(version_label)
        
        # 社交媒体链接 - 简单垂直显示网址
        content_layout.addWidget(QLabel("https://www.sihuangtech.com"))
        content_layout.addWidget(QLabel("mailto:developer@skstudio.cn"))
        content_layout.addWidget(QLabel("https://github.com/sihuangtech"))
        
        # 版权信息 - macOS风格
        copyright_label = QLabel('Copyright © 2025 SK Studio')
        copyright_label.setStyleSheet("""
            font-size: 9px;
            color: #666666;
            padding-top: 4px;
        """)
        content_layout.addWidget(copyright_label)
        
        # 确定按钮
        ok_button = QPushButton(tr('ok', 'OK'))
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        content_layout.addWidget(ok_button)
        
        # 将内容区域添加到主布局
        main_layout.addLayout(content_layout)
    


    def set_fixed_size(self):
        """设置固定大小 (macOS风格尺寸)"""
        self.setFixedSize(280, 200)  # 简化布局后的尺寸
        self.setMaximumSize(280, 200)
    
    def showEvent(self, event):
        """显示事件 - 居中对话框"""
        super().showEvent(event)
        if self.parent():
            parent_geo = self.parent().geometry()
            self.move(
                parent_geo.center().x() - self.width() // 2,
                parent_geo.center().y() - self.height() // 2
            )

def show_about_dialog(parent=None):
    """显示关于对话框的便捷函数"""
    dialog = AboutDialog(parent)
    dialog.exec()