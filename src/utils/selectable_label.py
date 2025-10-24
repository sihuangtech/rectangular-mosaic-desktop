# -*- coding: utf-8 -*-
"""
SelectableLabel 模块

用途：
    自定义 QLabel，用于在显示图片的同时绘制用户框选的矩形区域。

使用场景：
    被 MosaicTool 作为图片显示控件使用，实现框选实时可视化。
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent
from PySide6.QtCore import Qt, QRect, Signal, QPoint
from src.constants.config import SELECTION_BORDER_COLOR, SELECTION_BORDER_WIDTH

class SelectableLabel(QLabel):
    """
    可绘制选区的 QLabel。

    属性：
        selection_rect (QRect): 当前选区矩形（控件坐标系）
        is_selecting (bool): 是否处于正在框选状态，用于确定笔样式（虚线/实线）。
    """

    # 信号定义
    selection_completed = Signal(QRect)  # 选择完成信号
    selection_changed = Signal(QRect)    # 选择改变信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selection_rect: QRect | None = None
        self.is_selecting: bool = False
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)  # 启用鼠标跟踪

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

    def mousePressEvent(self, event: QMouseEvent):
        """
        鼠标按下事件：开始框选。
        """
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.is_selecting = True
            self.set_selection(QRect(self.start_point, self.start_point), True)
            self.selection_changed.emit(self.selection_rect)

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        鼠标移动事件：更新框选区域。
        """
        if self.is_selecting and hasattr(self, 'start_point'):
            current_rect = QRect(self.start_point, event.pos())
            self.set_selection(current_rect, True)
            self.selection_changed.emit(self.selection_rect)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        鼠标释放事件：完成框选。
        """
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            if self.selection_rect and not self.selection_rect.isNull():
                self.set_selection(self.selection_rect, False)
                self.selection_completed.emit(self.selection_rect)

    def get_selection_rect(self):
        """
        获取选择区域矩形。
        返回：
            QRect: 选择区域矩形，如果没有选择则返回空QRect
        """
        return self.selection_rect if self.selection_rect else QRect()

    def clear_selection(self):
        """
        清除选择区域。
        """
        self.set_selection(None, False)
        self.selection_changed.emit(QRect())