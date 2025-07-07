# -*- coding: utf-8 -*-
"""
马赛克处理逻辑模块

用途：
    提供对图片指定区域进行马赛克处理的函数。

使用场景：
    被主界面调用，对用户框选区域应用马赛克。
"""
from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import QRect

def apply_mosaic(image: QImage, rect: QRect, block_size: int = 15) -> QImage:
    """
    对指定矩形区域应用马赛克效果。
    参数：
        image (QImage): 原始图片
        rect (QRect): 需要马赛克的区域（图片坐标系）
        block_size (int): 马赛克块大小，默认15
    返回：
        QImage: 处理后的图片
    使用示例：
        new_img = apply_mosaic(image, QRect(10,10,100,100), 20)
    """
    if image is None or rect is None:
        return image
    img = image.copy()
    for y in range(rect.top(), rect.bottom(), block_size):
        for x in range(rect.left(), rect.right(), block_size):
            # 取块左上角像素颜色
            color = QColor(img.pixel(x, y))
            for dy in range(block_size):
                for dx in range(block_size):
                    px = x + dx
                    py = y + dy
                    if rect.contains(px, py) and px < img.width() and py < img.height():
                        img.setPixel(px, py, color.rgb())
    return img 