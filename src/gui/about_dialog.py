# -*- coding: utf-8 -*-
"""
关于对话框模块 - 显示应用程序信息
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from src.localization import tr
from src.constants.config import APP_VERSION, APP_BUILD_NUMBER, ORGANIZATION_NAME, APP_NAME
import os
import sys


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
        
        # 主布局 - 垂直布局：仅显示内容
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)  # 内容项之间的间距
        main_layout.setContentsMargins(30, 20, 30, 20)  # macOS风格边距
        
        # 内容区域
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)  # 内容项之间的紧凑间距
        
        # 应用名称 - macOS风格字体
        app_name_label = QLabel(APP_NAME)
        app_name_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #333333;
        """)
        content_layout.addWidget(app_name_label)
        
        # 版本信息 - 包含构建版本
        version_label = QLabel(f"Version {APP_VERSION}({APP_BUILD_NUMBER})")
        version_label.setStyleSheet("""
            font-size: 11px;
            color: #666666;
        """)
        content_layout.addWidget(version_label)
        
        # 超链接区域 - 分两行排列
        # 第一行：主要链接
        main_links_layout = QHBoxLayout()
        main_links_layout.setSpacing(8)  # 链接之间的间距
        
        # Website链接
        website_label = QLabel('<a href="https://www.sihuangtech.com">Website</a>')
        website_label.setOpenExternalLinks(True)
        website_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        main_links_layout.addWidget(website_label)
        
        # Email链接
        email_label = QLabel('<a href="mailto:developer@skstudio.cn">Email</a>')
        email_label.setOpenExternalLinks(True)
        email_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        main_links_layout.addWidget(email_label)
        
        # GitHub链接
        github_label = QLabel('<a href="https://github.com/sihuangtech">GitHub</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        main_links_layout.addWidget(github_label)
        
        main_links_layout.addStretch()  # 右侧填充
        content_layout.addLayout(main_links_layout)
        
        # 第二行：社交媒体链接
        social_links_layout = QHBoxLayout()
        social_links_layout.setSpacing(8)  # 链接之间的间距
        
        # 微博链接
        weibo_label = QLabel('<a href="https://www.weibo.com/u/7973019346">新浪微博</a>')
        weibo_label.setOpenExternalLinks(True)
        weibo_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        social_links_layout.addWidget(weibo_label)
        
        # 哔哩哔哩链接
        bilibili_label = QLabel('<a href="https://space.bilibili.com/3461571323889732">哔哩哔哩</a>')
        bilibili_label.setOpenExternalLinks(True)
        bilibili_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        social_links_layout.addWidget(bilibili_label)
        
        # X (Twitter)链接
        x_label = QLabel('<a href="https://x.com/SnakeKongStudio">X (Twitter)</a>')
        x_label.setOpenExternalLinks(True)
        x_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        social_links_layout.addWidget(x_label)
        
        # YouTube链接
        youtube_label = QLabel('<a href="https://www.youtube.com/@SnakeKonginchristStudio">YouTube</a>')
        youtube_label.setOpenExternalLinks(True)
        youtube_label.setStyleSheet("font-size: 11px; color: #0066cc; text-decoration: none;")
        social_links_layout.addWidget(youtube_label)
        
        social_links_layout.addStretch()  # 右侧填充
        content_layout.addLayout(social_links_layout)
        
        # 版权信息 - macOS风格
        copyright_label = QLabel(f'Copyright © 2025 {ORGANIZATION_NAME}')
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
        self.setFixedSize(280, 240)  # 增加高度以容纳两行链接
        self.setMaximumSize(280, 240)
    
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