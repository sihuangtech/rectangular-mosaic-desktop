# -*- coding: utf-8 -*-
"""
马赛克工具主窗口 - 重构版本
通过外部模块实现业务逻辑，主窗口只负责协调
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QSplitter, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import os

from src.localization import tr, set_language, LANGUAGES
from src.gui.ui_components import ControlPanel
from src.gui.menu_bar import AppMenuBar
from src.gui.status_bar import AppStatusBar
from src.gui.image_viewer import ImageViewer
from src.gui.ui_state_manager import UIStateManager
from src.features.file_manager import FileManager
from src.features.edit_history import EditHistory
from src.constants.config import (
    MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT,
    APP_VERSION_DISPLAY, UI_CONTROL_PANEL_WIDTH
)


class MainWindow(QMainWindow):
    """主窗口 - 通过外部模块处理业务逻辑"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化所有管理器 - 它们将处理具体的业务逻辑
        self.ui_state_manager = UIStateManager(self)
        self.file_manager = FileManager(self)
        self.history = EditHistory()
        
        # UI组件将在init_ui中创建
        self.control_panel = None
        self.image_viewer = None
        self.menu_bar = None
        self.status_bar = None
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面 - 只负责UI布局"""
        self.setWindowTitle(tr('app_name'))
        self.setWindowIcon(self.load_app_icon())
        self.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.setMinimumSize(MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT)
        self.setAcceptDrops(True)
        
        # 创建UI组件
        self.menu_bar = AppMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        self.status_bar = AppStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 创建中央布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        self.control_panel = ControlPanel()
        self.control_panel.setMinimumWidth(UI_CONTROL_PANEL_WIDTH)
        
        self.image_viewer = ImageViewer()
        
        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.image_viewer)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def load_app_icon(self):
        """加载应用图标"""
        import sys
        import platform
        
        # 获取图标目录
        if getattr(sys, 'frozen', False):
            icon_dir = os.path.join(sys._MEIPASS, 'assets')
        else:
            icon_dir = 'assets' if os.path.exists('assets') else \
                      os.path.join(os.path.dirname(__file__), '../../assets')
        
        # 根据操作系统选择图标文件
        icon_files = ['icon.ico', 'icon.png'] if platform.system() == 'Windows' else \
                    ['icon.icns', 'icon.png', 'icon.ico']
        
        # 查找存在的图标文件
        for icon_file in icon_files:
            icon_path = os.path.join(icon_dir, icon_file)
            if os.path.exists(icon_path):
                return QIcon(icon_path)
        
        return QIcon()
    
    def setup_connections(self):
        """设置信号连接 - 使用UIStateManager统一管理状态"""
        
        # 连接UIStateManager的信号到各个组件
        self.ui_state_manager.image_state_changed.connect(self.control_panel.update_button_states)
        self.ui_state_manager.image_state_changed.connect(self.menu_bar.update_menu_states)
        self.ui_state_manager.image_state_changed.connect(self.status_bar.update_status)
        
        self.ui_state_manager.history_state_changed.connect(lambda can_undo, can_redo: 
            self.control_panel.update_button_states(self.ui_state_manager.get_image_state(), can_undo, can_redo))
        self.ui_state_manager.history_state_changed.connect(lambda can_undo, can_redo:
            self.menu_bar.update_menu_states(self.ui_state_manager.get_image_state(), can_undo, can_redo))
        self.ui_state_manager.history_state_changed.connect(lambda can_undo, can_redo:
            self.status_bar.update_status(self.ui_state_manager.get_image_state(), can_undo, can_redo))
        
        # 连接控制面板的用户操作到业务逻辑
        self.control_panel.open_image_clicked.connect(self.handle_open_image)
        self.control_panel.save_image_clicked.connect(self.handle_save_image)
        self.control_panel.undo_clicked.connect(self.handle_undo)
        self.control_panel.redo_clicked.connect(self.handle_redo)
        self.control_panel.clear_clicked.connect(self.handle_clear_selection)
        self.control_panel.block_size_changed.connect(self.ui_state_manager.set_block_size)
        self.control_panel.intensity_changed.connect(self.ui_state_manager.set_intensity)
        
        # 连接菜单栏的用户操作
        self.menu_bar.open_image_triggered.connect(self.handle_open_image)
        self.menu_bar.save_image_triggered.connect(self.handle_save_image)
        self.menu_bar.undo_triggered.connect(self.handle_undo)
        self.menu_bar.redo_triggered.connect(self.handle_redo)
        self.menu_bar.clear_triggered.connect(self.handle_clear_selection)
        self.menu_bar.language_changed.connect(self.handle_language_change)
        self.menu_bar.about_triggered.connect(self.show_about)
        self.menu_bar.exit_triggered.connect(self.close)
        
        # 连接图像查看器的信号
        self.image_viewer.selection_made.connect(self.handle_selection_made)
        self.image_viewer.image_loaded.connect(self.handle_image_loaded)
        
        # 初始化状态
        self.update_ui_state()
    
    def update_ui_state(self):
        """更新UI状态 - 通过UIStateManager统一管理"""
        # UIStateManager会自动发出信号，各个组件会相应更新
        pass
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            tr('about'),
            tr('about_text').format(APP_VERSION_DISPLAY)
        )
    
    def handle_open_image(self):
        """处理打开图像 - 使用FileManager"""
        self.file_manager.open_image_file()
        
    def handle_save_image(self):
        """处理保存图像 - 使用FileManager"""
        self.file_manager.save_image_file()
        
    def handle_undo(self):
        """处理撤销 - 使用EditHistory"""
        self.history.undo()
        
    def handle_redo(self):
        """处理重做 - 使用EditHistory"""
        self.history.redo()
        
    def handle_clear_selection(self):
        """处理清除选择 - 使用ImageViewer"""
        self.image_viewer.clear_selection()
    
    def on_block_size_changed(self, value):
        """块大小改变处理"""
        self.block_size = value
        self.ui_state_manager.set_block_size(value)
        self.status_bar.show_message(tr('block_size_changed').format(value))
    
    def handle_language_change(self, language_code):
        """处理语言切换 - 使用Translator类"""
        set_language(language_code)
    
    def handle_selection_made(self, rect):
        """处理选择区域 - 使用UIStateManager和ImageViewer"""
        self.ui_state_manager.set_selection_state(True)
        # 应用马赛克逻辑在ImageViewer中处理
        
    def handle_image_loaded(self, image_path):
        """处理图像加载 - 使用UIStateManager"""
        self.ui_state_manager.set_image_state(True)
    
    def change_language(self, language_code):
        """切换语言 - 使用Translator类"""
        if set_language(language_code):
            # 重新翻译UI
            self.retranslate_ui()
    
    def retranslate_ui(self):
        """重新翻译UI - 使用Translator类"""
        self.setWindowTitle(tr('app_name'))
        
        # 重新创建菜单栏
        self.menuBar().clear()
        self.menu_bar = AppMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # 重新连接信号
        self.setup_connections()
        
        # 更新状态
        self.update_ui_state()
    
    def dragEnterEvent(self, event):
        """拖拽进入事件 - 使用FileManager验证文件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile():
                file_path = urls[0].toLocalFile()
                if self.file_manager.is_valid_image_file(file_path):
                    event.acceptProposedAction()
    
    def dropEvent(self, event):
        """拖拽放下事件 - 使用FileManager打开文件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile():
                file_path = urls[0].toLocalFile()
                if self.file_manager.is_valid_image_file(file_path):
                    self.file_manager.open_image_file(file_path)