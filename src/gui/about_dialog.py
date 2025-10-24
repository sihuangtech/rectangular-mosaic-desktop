# -*- coding: utf-8 -*-
"""
关于对话框模块 - 显示应用程序信息
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from src.localization import tr
from src.constants.config import APP_VERSION_DISPLAY
import os


class AboutDialog(QDialog):
    """关于对话框类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.set_fixed_size()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(tr('about', 'About'))
        self.setModal(True)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 应用图标
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
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
        
        main_layout.addWidget(icon_label)
        
        # 应用名称
        app_name_label = QLabel(tr('app_name', 'Rectangular Mosaic'))
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        main_layout.addWidget(app_name_label)
        
        # 版本信息
        version_label = QLabel(f"版本 {APP_VERSION_DISPLAY}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 10px;")
        main_layout.addWidget(version_label)
        
        # 描述信息
        description_label = QLabel(
            "矩形马赛克桌面应用\n"
            "一个简单易用的图像马赛克处理工具"
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 15px;")
        description_label.setWordWrap(True)
        main_layout.addWidget(description_label)
        
        # 功能特性
        features_text = QTextEdit()
        features_text.setPlainText(
            "主要功能：\n"
            "• 支持常见图片格式（PNG、JPEG等）\n"
            "• 矩形区域选择和马赛克处理\n"
            "• 可调节马赛克块大小\n"
            "• 撤销/重做功能\n"
            "• 跨平台支持（Windows/macOS/Linux）"
        )
        features_text.setReadOnly(True)
        features_text.setMaximumHeight(120)
        features_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 11px;
                color: #555;
            }
        """)
        main_layout.addWidget(features_text)
        
        # 版权信息
        copyright_label = QLabel("© 2025 彩旗工作室")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 10px; color: #999; margin-top: 10px;")
        main_layout.addWidget(copyright_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 确定按钮
        ok_button = QPushButton(tr('ok', 'OK'))
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def set_fixed_size(self):
        """设置固定大小"""
        self.setFixedSize(400, 450)
        self.setMaximumSize(400, 450)
    
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