# -*- coding: utf-8 -*-
"""
SelectableLabel 模块

用途：
    自定义 QLabel，用于在显示图片的同时绘制用户框选的矩形区域。

使用场景：
    被 MosaicTool 作为图片显示控件使用，实现框选实时可视化。
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect
from src.constants.config import SELECTION_BORDER_COLOR, SELECTION_BORDER_WIDTH

class SelectableLabel(QLabel):
    """
    可绘制选区的 QLabel。

    属性：
        selection_rect (QRect): 当前选区矩形（控件坐标系）
        is_selecting (bool): 是否处于正在框选状态，用于确定笔样式（虚线/实线）。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selection_rect: QRect | None = None
        self.is_selecting: bool = False
        self.setAlignment(Qt.AlignCenter)

    def set_selection(self, rect: QRect | None, selecting: bool):
        """
        设置选区并刷新显示。
        参数：
            rect (QRect | None): 选区矩形，None 表示清除
            selecting (bool): True 表示正在框选（虚线），False 表示框选完成（实线）
        """
        self.selection_rect = rect
        self.is_selecting = selecting
        self.update()

    def paintEvent(self, event):
        """
        重绘事件：先调用父类绘制图片，再绘制选区矩形。
        """
        super().paintEvent(event)
        if self.selection_rect and not self.selection_rect.isNull():
            painter = QPainter(self)
            pen_style = Qt.DashLine if self.is_selecting else Qt.SolidLine
            pen = QPen(QColor(*SELECTION_BORDER_COLOR), SELECTION_BORDER_WIDTH, pen_style)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)
            painter.end()