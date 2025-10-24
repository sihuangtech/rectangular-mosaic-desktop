"""
文件管理模块 - 处理图像文件的打开和保存操作
"""
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QImage
from PySide6.QtCore import QObject, Signal
from src.localization import tr
from src.features.image_loader import load_image, save_image
from src.constants.config import SUPPORTED_IMAGE_EXTENSIONS, SUPPORTED_SAVE_EXTENSIONS


class FileManager(QObject):
    """文件管理器类"""
    image_opened = Signal(QImage, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        self.parent_widget = parent
        self.valid_extensions = SUPPORTED_IMAGE_EXTENSIONS

    def open_image_file(self, file_path=None):
        """
        打开图像文件。
        如果提供了 file_path，则直接打开；否则，显示文件对话框。
        Args:
            file_path (str, optional): 要打开的图像文件路径. Defaults to None.
        """
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent_widget,
                tr("open_image", "Open Image"),
                "",
                f"Image Files ({' '.join(['*' + ext for ext in self.valid_extensions])});;All Files (*)"
            )

        if file_path:
            if not self.is_valid_image_file(file_path):
                QMessageBox.critical(
                    self.parent_widget,
                    tr("error", "Error"),
                    tr("invalid_file_format", "Invalid file format")
                )
                return

            # 使用统一的load_image函数
            image = load_image(file_path)
            if image is None:
                QMessageBox.critical(
                    self.parent_widget,
                    tr("error", "Error"),
                    tr("failed_to_load_image", "Failed to load image")
                )
                return

            self.current_file_path = file_path
            self.image_opened.emit(image, file_path)

    def save_image_file(self, image, parent_widget):
        """
        保存图像文件 - 使用统一的save_image函数
        Args:
            image: 要保存的图像
            parent_widget: 父窗口部件
        Returns:
            bool: 是否成功保存
        """
        if image is None:
            return False
        
        file_path, _ = QFileDialog.getSaveFileName(
            parent_widget,
            tr("save_image", "Save Image"),
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        if file_path:
            # 确保文件有正确的扩展名
            if not file_path.lower().endswith(tuple(SUPPORTED_SAVE_EXTENSIONS)):
                file_path += '.png'
            
            # 使用统一的save_image函数
            if save_image(image, file_path):
                self.current_file_path = file_path
                return True
            else:
                QMessageBox.critical(
                    parent_widget,
                    tr("error", "Error"),
                    tr("failed_to_save_image", "Failed to save image")
                )
                return False
        
        return False
    
    def get_current_file_name(self):
        """获取当前文件名（不含路径）"""
        if self.current_file_path:
            return os.path.basename(self.current_file_path)
        return None
    
    def get_current_file_path(self):
        """获取当前文件完整路径"""
        return self.current_file_path