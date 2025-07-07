# -*- coding: utf-8 -*-
"""
图片加载与保存模块

用途：
    提供图片的加载和保存功能。

使用场景：
    被主界面调用，实现图片的打开与保存。
"""
from PySide6.QtGui import QImage

def load_image(file_path: str) -> QImage:
    """
    加载图片文件。
    参数：
        file_path (str): 图片文件路径
    返回：
        QImage: 加载的图片对象
    """
    image = QImage(file_path)
    return image if not image.isNull() else None

def save_image(image: QImage, file_path: str) -> bool:
    """
    保存图片到文件。
    参数：
        image (QImage): 要保存的图片对象
        file_path (str): 保存路径
    返回：
        bool: 保存是否成功
    """
    if image is None:
        return False
    return image.save(file_path) 