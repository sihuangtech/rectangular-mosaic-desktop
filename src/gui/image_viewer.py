# -*- coding: utf-8 -*-
"""
图像显示组件模块 - 包含图像显示和选择功能
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from src.utils.selectable_label import SelectableLabel
from src.localization import tr
from src.features.image_loader import load_image
from src.constants.config import (
    IMAGE_VIEWER_MIN_WIDTH, IMAGE_VIEWER_MIN_HEIGHT, IMAGE_VIEWER_BACKGROUND_COLOR, IMAGE_VIEWER_BORDER_STYLE
)


class ImageViewer(QWidget):
    """图像查看器组件"""
    
    # 信号定义
    selection_made = Signal(object)  # 发出选择区域
    image_loaded = Signal(str)  # 发出图像路径
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image = None
        self.original_image = None
        self.image_path = None
        self.init_ui()
    
    def init_ui(self):
        """初始化图像查看器UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)
        
        # 创建可选择的标签
        self.image_label = SelectableLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(IMAGE_VIEWER_MIN_WIDTH, IMAGE_VIEWER_MIN_HEIGHT)
        self.image_label.setStyleSheet(f"QLabel {{ background-color: {IMAGE_VIEWER_BACKGROUND_COLOR}; border: {IMAGE_VIEWER_BORDER_STYLE}; }}")
        self.image_label.selection_completed.connect(self.on_selection_completed)
        
        scroll_area.setWidget(self.image_label)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def load_image(self, file_path):
        """加载图像文件 - 使用统一的image_loader"""
        try:
            # 使用统一的load_image函数
            image = load_image(file_path)
            if image is None:
                raise ValueError(f"无法加载图片: {file_path}")
            
            # 保存原始图像
            self.original_image = image.copy()
            self.current_image = image.copy()
            self.image_path = file_path
            
            # 显示图片
            self.display_image(image)
            self.image_loaded.emit(file_path)
            
            return True
            
        except Exception as e:
            QMessageBox.critical(
                self,
                tr("error", "Error"),
                f"{tr('load_failed', 'Load failed')}: {str(e)}"
            )
            return False
    
    def display_image(self, image):
        """在标签中显示图像，根据窗口大小自动缩放"""
        if image and not image.isNull():
            # 获取标签的当前尺寸
            label_size = self.image_label.size()
            
            # 如果标签还没有尺寸，使用最小尺寸
            if label_size.width() <= 1 or label_size.height() <= 1:
                label_size.setWidth(IMAGE_VIEWER_MIN_WIDTH)
                label_size.setHeight(IMAGE_VIEWER_MIN_HEIGHT)
            
            # 将图像缩放到适合标签的大小，保持纵横比
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.adjustSize()
    
    def get_selection_rect(self):
        """获取选择区域 - 转换为原始图像坐标"""
        display_rect = self.image_label.get_selection_rect()
        if not display_rect or display_rect.isNull():
            return display_rect
        
        # 获取显示的图片尺寸
        pixmap = self.image_label.pixmap()
        if not pixmap or pixmap.isNull():
            return display_rect
        
        # 获取原始图像尺寸
        if not self.has_image():
            return display_rect
        
        original_width = self.current_image.width()
        original_height = self.current_image.height()
        display_width = pixmap.width()
        display_height = pixmap.height()
        
        # 计算缩放比例
        scale_x = original_width / display_width
        scale_y = original_height / display_height
        
        # 转换坐标到原始图像（display_rect已经是图片相对坐标）
        from PySide6.QtCore import QRect
        original_rect = QRect(
            int(display_rect.x() * scale_x),
            int(display_rect.y() * scale_y),
            int(display_rect.width() * scale_x),
            int(display_rect.height() * scale_y)
        )
        
        return original_rect
    
    def clear_selection(self):
        """清除选择区域"""
        self.image_label.clear_selection()
    
    def clear_image(self):
        """清除图像"""
        # 清除当前图像
        self.current_image = None
        self.original_image = None
        self.image_path = None
        
        # 清除标签中的图像
        self.image_label.clear()
        
        # 清除选择区域
        self.clear_selection()
    
    def has_image(self):
        """检查是否有图像加载"""
        return self.current_image is not None and not self.current_image.isNull()
    
    def get_current_image(self):
        """获取当前图像"""
        return self.current_image
    
    def get_original_image(self):
        """获取原始图像"""
        return self.original_image
    
    def update_image(self, new_image):
        """更新当前图像"""
        self.current_image = new_image.copy()
        self.display_image(new_image)
    
    def on_selection_completed(self, rect):
        """选择完成处理"""
        if rect and rect.isValid():
            self.selection_made.emit(rect)
    
    def get_image_size(self):
        """获取图像尺寸"""
        if self.has_image():
            return self.current_image.width(), self.current_image.height()
        return 0, 0
    
    def resizeEvent(self, event):
        """窗口大小改变时重新调整图片大小"""
        super().resizeEvent(event)
        # 如果有图片，重新显示以适应新的大小
        if self.has_image() and self.current_image:
            self.display_image(self.current_image)