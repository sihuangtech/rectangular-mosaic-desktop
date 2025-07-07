# -*- coding: utf-8 -*-
"""
矩形框选工具模块

用途：
    提供矩形框选的逻辑，处理鼠标事件并记录选区。

使用场景：
    被主界面调用，实现鼠标拖拽框选区域。
"""
from PySide6.QtCore import QPoint, QRect

class RectSelector:
    """
    矩形框选工具类，记录框选起止点并生成 QRect。
    """
    def __init__(self):
        self.start_point = None  # 框选起点 QPoint
        self.end_point = None    # 框选终点 QPoint
        self.selecting = False  # 是否正在框选

    def start(self, point: QPoint):
        """
        开始框选。
        参数：
            point (QPoint): 框选起点
        """
        self.start_point = point
        self.end_point = point
        self.selecting = True

    def update(self, point: QPoint):
        """
        更新框选终点。
        参数：
            point (QPoint): 当前鼠标点
        """
        if self.selecting:
            self.end_point = point

    def finish(self, point: QPoint):
        """
        完成框选。
        参数：
            point (QPoint): 框选终点
        """
        if self.selecting:
            self.end_point = point
            self.selecting = False

    def get_rect(self) -> QRect:
        """
        获取当前框选区域。
        返回：
            QRect: 框选区域矩形
        """
        if self.start_point and self.end_point:
            return QRect(self.start_point, self.end_point)
        return QRect() 