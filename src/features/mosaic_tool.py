# -*- coding: utf-8 -*-
"""
主界面与功能入口模块

用途：
    提供图片上传、显示、矩形框选、马赛克处理等主要功能的界面和交互逻辑。

使用场景：
    作为 PySide6 应用的主窗口模块被 main.py 调用。
"""
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QSlider
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QIcon
from PySide6.QtCore import Qt, QRect, QPoint
import os
from src.features.image_loader import load_image, save_image
from src.features.image_mosaic import apply_mosaic
from src.utils.rect_selector import RectSelector
from src.constants.config import DEFAULT_MOSAIC_BLOCK_SIZE, MIN_MOSAIC_BLOCK_SIZE, MAX_MOSAIC_BLOCK_SIZE, APP_NAME
from src.utils.selectable_label import SelectableLabel

class MosaicTool(QMainWindow):
    """
    主窗口类，负责图片加载、显示、框选和马赛克处理的交互逻辑。
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        # 自动加载应用图标（兼容 PyInstaller 打包和源码运行）
        import sys
        import platform
        def get_icon_path():
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
                icon_dir = os.path.join(base_dir, 'assets')
            else:
                if os.path.exists('assets'):
                    icon_dir = 'assets'
                else:
                    base_dir = os.path.dirname(__file__)
                    icon_dir = os.path.abspath(os.path.join(base_dir, '../../assets'))
            current_os = platform.system()
            icon_candidates = []
            if current_os == 'Windows':
                icon_candidates = ['icon.ico', 'icon.png']
            elif current_os == 'Darwin':
                icon_candidates = ['icon.icns', 'icon.png', 'icon.ico']
            else:
                icon_candidates = ['icon.png', 'icon.ico']
            for fname in icon_candidates:
                fpath = os.path.join(icon_dir, fname)
                if os.path.exists(fpath):
                    return fpath
            return None
        icon_path = get_icon_path()
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        self.resize(1000, 700)  # 设置默认窗口大小
        # 使用可绘制选区的自定义 QLabel
        self.image_label = SelectableLabel()
        self.image = None  # 当前 QImage 对象
        self.pixmap = None  # 原始 QPixmap 对象
        self.display_pixmap = None  # 根据窗口缩放后的 QPixmap
        self.rect_selector = RectSelector()  # 框选工具
        self.mosaic_rect = None  # 选中的矩形区域 QRect
        self.history: list[QImage] = []  # 历史栈用于撤销
        self.init_ui()
        self.setAcceptDrops(True)  # 允许窗口接受拖拽

    def init_ui(self):
        """
        初始化界面布局和按钮。
        """
        open_btn = QPushButton("上传图片")
        open_btn.clicked.connect(self.open_image)
        save_btn = QPushButton("保存图片")
        save_btn.clicked.connect(self.save_image)
        mosaic_btn = QPushButton("区域马赛克")
        mosaic_btn.clicked.connect(self.apply_mosaic_to_rect)
        mosaic_btn.setEnabled(False)
        self.mosaic_btn = mosaic_btn
        # 撤销按钮
        undo_btn = QPushButton("撤销")
        undo_btn.clicked.connect(self.undo_last)
        undo_btn.setEnabled(False)
        self.undo_btn = undo_btn

        # 块大小设置 SpinBox
        size_label = QLabel("块大小:")
        size_spin = QSpinBox()
        size_spin.setRange(MIN_MOSAIC_BLOCK_SIZE, MAX_MOSAIC_BLOCK_SIZE)
        size_spin.setValue(DEFAULT_MOSAIC_BLOCK_SIZE)

        # 滑块设置
        size_slider = QSlider(Qt.Horizontal)
        size_slider.setRange(MIN_MOSAIC_BLOCK_SIZE, MAX_MOSAIC_BLOCK_SIZE)
        size_slider.setValue(DEFAULT_MOSAIC_BLOCK_SIZE)

        # 双向联动：SpinBox ↔ Slider
        size_spin.valueChanged.connect(size_slider.setValue)
        size_slider.valueChanged.connect(size_spin.setValue)

        self.size_spin = size_spin      # 保存引用供后续读取
        self.size_slider = size_slider  # 保存引用，便于扩展

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(mosaic_btn)
        btn_layout.addWidget(undo_btn)

        btn_layout.addStretch()
        btn_layout.addWidget(size_label)
        btn_layout.addWidget(size_spin)
        btn_layout.addWidget(size_slider)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_display_pixmap(self):
        """
        根据 QLabel 大小生成缩放后的 QPixmap，用于界面显示，保持原始 image 不变。
        """
        if self.image is None:
            return
        label_size = self.image_label.size()
        if label_size.width() == 0 or label_size.height() == 0:
            # 若组件尚未布局完成，直接使用原图
            self.display_pixmap = QPixmap.fromImage(self.image)
        else:
            self.display_pixmap = QPixmap.fromImage(self.image).scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

    def open_image(self):
        """
        打开图片文件并显示。
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", os.getcwd(), "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.current_image_path = file_path  # 记录当前图片路径
            self.image = load_image(file_path)
            if self.image is None:
                return
            self.pixmap = QPixmap.fromImage(self.image)
            self.update_display_pixmap()
            self.image_label.setPixmap(self.display_pixmap)
            self.image_label.set_selection(None, False)
            self.mosaic_btn.setEnabled(True)
            self.update()

    def save_image(self):
        """
        保存当前图片。
        优化：JPG格式排在PNG前，默认文件名为原图名。
        """
        if self.image is None:
            return
        # 获取当前图片文件名（如有）
        default_name = "output.jpg"
        if hasattr(self, 'current_image_path') and self.current_image_path:
            base = os.path.basename(self.current_image_path)
            name, _ = os.path.splitext(base)
            default_name = f"{name}.jpg"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            os.path.join(os.getcwd(), default_name),
            "JPEG Files (*.jpg *.jpeg);;PNG Files (*.png)"
        )
        if file_path:
            save_image(self.image, file_path)

    def mousePressEvent(self, event):
        """
        鼠标按下事件，开始框选。
        """
        if self.image is None:
            return
        if event.button() == Qt.LeftButton:
            # 使用 RectSelector 记录起点
            self.rect_selector.start(event.pos())
            # 初始化 label 选区（空矩形），用于实时显示虚线框
            self.image_label.set_selection(QRect(), True)
            self.update()

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件，更新框选区域。
        """
        if self.rect_selector.selecting:
            self.rect_selector.update(event.pos())
            # 更新 label 中的虚线框
            widget_rect = self.rect_selector.get_rect()
            label_rect = widget_rect.translated(-self.image_label.geometry().x(), -self.image_label.geometry().y())
            self.image_label.set_selection(label_rect, True)
            self.update()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件，完成框选。
        """
        if self.rect_selector.selecting and event.button() == Qt.LeftButton:
            self.rect_selector.finish(event.pos())
            # 记录框选区域
            widget_rect = self.rect_selector.get_rect()
            label_rect = widget_rect.translated(-self.image_label.geometry().x(), -self.image_label.geometry().y())
            self.image_label.set_selection(label_rect, False)
            self.mosaic_rect = self.get_image_rect_from_widget_rect(widget_rect.topLeft(), widget_rect.bottomRight())
            self.update()

    def paintEvent(self, event):
        """
        重绘事件，绘制框选、模板等所有高亮区域。
        """
        super().paintEvent(event)
        painter = QPainter(self)
        # 绘制当前框选
        if self.rect_selector.selecting and self.rect_selector.start_point and self.rect_selector.end_point:
            pen = QPen(QColor(255, 0, 0), 2, Qt.DashLine)
            painter.setPen(pen)
            rect = self.rect_selector.get_rect()
            painter.drawRect(rect)
        elif self.mosaic_rect:
            pen = QPen(QColor(0, 255, 0), 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self.mosaic_rect)
        painter.end()

    def get_image_rect_from_widget_rect(self, start: QPoint, end: QPoint):
        """
        将窗口坐标的矩形转换为图片坐标的矩形。
        参数：
            start (QPoint): 框选起点
            end (QPoint): 框选终点
        返回：
            QRect: 图片坐标系下的矩形区域
        """
        if self.image is None:
            return None
        # QLabel 在主窗口中的几何位置
        label_rect = self.image_label.geometry()

        # 将窗口坐标转换为 QLabel 内坐标
        lx1 = min(start.x(), end.x()) - label_rect.x()
        ly1 = min(start.y(), end.y()) - label_rect.y()
        lx2 = max(start.x(), end.x()) - label_rect.x()
        ly2 = max(start.y(), end.y()) - label_rect.y()

        # 当前显示的缩放后 pixmap 尺寸
        disp_w = self.display_pixmap.width()
        disp_h = self.display_pixmap.height()

        # 计算 pixmap 在 QLabel 中的偏移量（图片是居中显示的）
        offset_x = max((label_rect.width() - disp_w) // 2, 0)
        offset_y = max((label_rect.height() - disp_h) // 2, 0)

        # 将 QLabel 坐标转换为 pixmap 坐标
        px1 = lx1 - offset_x
        py1 = ly1 - offset_y
        px2 = lx2 - offset_x
        py2 = ly2 - offset_y

        # 裁剪到 pixmap 范围
        px1 = max(px1, 0)
        py1 = max(py1, 0)
        px2 = min(px2, disp_w)
        py2 = min(py2, disp_h)

        if px2 <= px1 or py2 <= py1:
            return None

        # 计算缩放比例，将 pixmap 坐标映射至原始图片坐标
        scale_x = self.image.width() / disp_w
        scale_y = self.image.height() / disp_h

        ix1 = int(px1 * scale_x)
        iy1 = int(py1 * scale_y)
        ix2 = int(px2 * scale_x)
        iy2 = int(py2 * scale_y)

        # 再次裁剪以防越界
        ix1 = max(min(ix1, self.image.width() - 1), 0)
        iy1 = max(min(iy1, self.image.height() - 1), 0)
        ix2 = max(min(ix2, self.image.width()), ix1 + 1)
        iy2 = max(min(iy2, self.image.height()), iy1 + 1)

        return QRect(ix1, iy1, ix2 - ix1, iy2 - iy1)

    def apply_mosaic_to_rect(self):
        """
        对选中区域应用马赛克效果。
        """
        if self.image is None or self.mosaic_rect is None:
            return
        # 将当前图像压入历史栈
        self.history.append(self.image.copy())
        self.undo_btn.setEnabled(True)
        block_size = self.size_spin.value()
        # 调用马赛克处理逻辑
        self.image = apply_mosaic(self.image, self.mosaic_rect, block_size)
        self.pixmap = QPixmap.fromImage(self.image)
        self.update_display_pixmap()
        self.image_label.setPixmap(self.display_pixmap)
        # 清除选区显示
        self.image_label.set_selection(None, False)
        self.update()

    def dragEnterEvent(self, event):
        """
        拖拽进入事件，判断是否为文件类型。
        """
        if event.mimeData().hasUrls():
            # 检查是否为图片文件
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        """
        拖拽释放事件，处理图片文件导入。
        """
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                self.image = load_image(file_path)
                if self.image is not None:
                    self.pixmap = QPixmap.fromImage(self.image)
                    self.update_display_pixmap()
                    self.image_label.setPixmap(self.display_pixmap)
                    self.image_label.set_selection(None, False)
                    self.mosaic_btn.setEnabled(True)
                    self.update()
                break

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image is not None:
            self.update_display_pixmap()
            self.image_label.setPixmap(self.display_pixmap)

    def update(self):
        """
        重绘界面。
        """
        self.update_display_pixmap()
        self.image_label.setPixmap(self.display_pixmap)
        self.repaint()

    def undo_last(self):
        """
        撤销上一次马赛克操作，恢复到上一状态。
        """
        if not self.history:
            return
        self.image = self.history.pop()
        if not self.history:
            self.undo_btn.setEnabled(False)
        self.pixmap = QPixmap.fromImage(self.image)
        self.update_display_pixmap()
        self.image_label.setPixmap(self.display_pixmap)
        # 清除选区
        self.mosaic_rect = None
        self.image_label.set_selection(None, False)
        self.update()