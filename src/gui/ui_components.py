# -*- coding: utf-8 -*-
"""
UI组件模块 - 包含MosaicTool的用户界面组件
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                                QSpinBox, QSlider, QLabel, QGroupBox, QComboBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from src.localization import tr
from src.constants.config import (
    UI_CONTROL_PANEL_WIDTH, UI_BLOCK_SIZE_SPIN_RANGE, UI_BLOCK_SIZE_SLIDER_RANGE,
    UI_BLOCK_SIZE_DEFAULT, UI_INTENSITY_SPIN_RANGE, UI_INTENSITY_SLIDER_RANGE,
    UI_INTENSITY_DEFAULT, UI_LAYOUT_SPACING, UI_LAYOUT_MARGIN
)


class ControlPanel(QWidget):
    """控制面板组件"""
    
    # 信号定义
    open_image_clicked = Signal()
    save_image_clicked = Signal()
    undo_clicked = Signal()
    redo_clicked = Signal()
    clear_clicked = Signal()
    apply_mosaic_clicked = Signal()
    block_size_changed = Signal(int)
    intensity_changed = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化控制面板UI"""
        layout = QVBoxLayout()
        layout.setSpacing(UI_LAYOUT_SPACING)
        layout.setContentsMargins(UI_LAYOUT_MARGIN, UI_LAYOUT_MARGIN, UI_LAYOUT_MARGIN, UI_LAYOUT_MARGIN)
        
        # 文件操作组
        file_group = self.create_file_group()
        layout.addWidget(file_group)
        
        # 编辑操作组
        edit_group = self.create_edit_group()
        layout.addWidget(edit_group)
        
        # 参数控制组
        params_group = self.create_params_group()
        layout.addWidget(params_group)
        
        # 添加弹簧
        layout.addStretch()
        
        self.setLayout(layout)
        self.setFixedWidth(UI_CONTROL_PANEL_WIDTH)
    
    def create_file_group(self):
        """创建文件操作组"""
        group = QGroupBox(tr("file", "File"))
        layout = QVBoxLayout()
        
        # 打开图片按钮
        self.open_btn = QPushButton(tr("open_image", "Open Image"))
        self.open_btn.clicked.connect(self.open_image_clicked.emit)
        layout.addWidget(self.open_btn)
        
        # 保存图片按钮
        self.save_btn = QPushButton(tr("save_image", "Save Image"))
        self.save_btn.clicked.connect(self.save_image_clicked.emit)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)
        
        group.setLayout(layout)
        return group
    
    def create_edit_group(self):
        """创建编辑操作组"""
        group = QGroupBox(tr("edit", "Edit"))
        layout = QVBoxLayout()
        
        # 应用马赛克按钮
        self.apply_mosaic_btn = QPushButton(tr("apply_mosaic", "Apply Mosaic"))
        self.apply_mosaic_btn.clicked.connect(self.apply_mosaic_clicked.emit)
        self.apply_mosaic_btn.setEnabled(False)
        layout.addWidget(self.apply_mosaic_btn)
        
        # 撤销按钮
        self.undo_btn = QPushButton(tr("undo", "Undo"))
        self.undo_btn.clicked.connect(self.undo_clicked.emit)
        self.undo_btn.setEnabled(False)
        layout.addWidget(self.undo_btn)
        
        # 重做按钮
        self.redo_btn = QPushButton(tr("redo", "Redo"))
        self.redo_btn.clicked.connect(self.redo_clicked.emit)
        self.redo_btn.setEnabled(False)
        layout.addWidget(self.redo_btn)
        
        # 清除按钮
        self.clear_btn = QPushButton(tr("clear", "Clear"))
        self.clear_btn.clicked.connect(self.clear_clicked.emit)
        self.clear_btn.setEnabled(False)
        layout.addWidget(self.clear_btn)
        
        group.setLayout(layout)
        return group
    
    def create_params_group(self):
        """创建参数控制组"""
        group = QGroupBox(tr("settings", "Settings"))
        layout = QVBoxLayout()
        
        # 块大小控制
        block_layout = QHBoxLayout()
        block_layout.addWidget(QLabel(tr("block_size", "Block Size")))
        
        self.block_size_spin = QSpinBox()
        self.block_size_spin.setRange(*UI_BLOCK_SIZE_SPIN_RANGE)
        self.block_size_spin.setValue(UI_BLOCK_SIZE_DEFAULT)
        self.block_size_spin.valueChanged.connect(self.block_size_changed.emit)
        block_layout.addWidget(self.block_size_spin)
        
        layout.addLayout(block_layout)
        
        # 块大小滑块
        self.block_size_slider = QSlider(Qt.Horizontal)
        self.block_size_slider.setRange(*UI_BLOCK_SIZE_SLIDER_RANGE)
        self.block_size_slider.setValue(UI_BLOCK_SIZE_DEFAULT)
        self.block_size_slider.valueChanged.connect(self.on_block_slider_changed)
        layout.addWidget(self.block_size_slider)
        
        # 强度控制
        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(QLabel(tr("intensity", "Intensity")))
        
        self.intensity_spin = QSpinBox()
        self.intensity_spin.setRange(*UI_INTENSITY_SPIN_RANGE)
        self.intensity_spin.setValue(UI_INTENSITY_DEFAULT)
        self.intensity_spin.valueChanged.connect(self.intensity_changed.emit)
        intensity_layout.addWidget(self.intensity_spin)
        
        layout.addLayout(intensity_layout)
        
        # 强度滑块
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(*UI_INTENSITY_SLIDER_RANGE)
        self.intensity_slider.setValue(UI_INTENSITY_DEFAULT)
        self.intensity_slider.valueChanged.connect(self.on_intensity_slider_changed)
        layout.addWidget(self.intensity_slider)
        
        group.setLayout(layout)
        return group
    
    def on_block_slider_changed(self, value):
        """块大小滑块变化处理"""
        self.block_size_spin.setValue(value)
        self.block_size_changed.emit(value)
    
    def on_intensity_slider_changed(self, value):
        """强度滑块变化处理"""
        self.intensity_spin.setValue(value)
        self.intensity_changed.emit(value)
    
    def update_button_states(self, has_image=False, can_undo=False, can_redo=False, has_selection=False):
        """更新按钮状态"""
        self.save_btn.setEnabled(has_image)
        self.undo_btn.setEnabled(can_undo)
        self.redo_btn.setEnabled(can_redo)
        self.clear_btn.setEnabled(has_image)
        self.apply_mosaic_btn.setEnabled(has_image and has_selection)
    
    def get_block_size(self):
        """获取块大小"""
        return self.block_size_spin.value()
    
    def get_intensity(self):
        """获取强度值"""
        return self.intensity_spin.value()


class LanguageSelector(QWidget):
    """语言选择器组件"""
    
    language_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化语言选择器UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(UI_LAYOUT_MARGIN, UI_LAYOUT_MARGIN, UI_LAYOUT_MARGIN, UI_LAYOUT_MARGIN)
        
        label = QLabel(tr("language", "Language"))
        layout.addWidget(label)
        
        self.language_combo = QComboBox()
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        layout.addWidget(self.language_combo)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def populate_languages(self, languages):
        """填充语言列表"""
        self.language_combo.clear()
        for lang_code in languages:
            self.language_combo.addItem(lang_code, lang_code)
    
    def set_current_language(self, language_code):
        """设置当前语言"""
        index = self.language_combo.findData(language_code)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
    
    def on_language_changed(self, text):
        """语言变化处理"""
        language_code = self.language_combo.currentData()
        if language_code:
            self.language_changed.emit(language_code)
    
    def get_current_language(self):
        """获取当前语言"""
        return self.language_combo.currentData()