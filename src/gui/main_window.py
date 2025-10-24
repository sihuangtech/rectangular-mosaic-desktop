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
    MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT, UI_CONTROL_PANEL_WIDTH
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
        
        # 初始化主题管理器并应用主题
        from src.gui.theme_manager import get_theme_manager
        theme_manager = get_theme_manager()
        theme_manager.apply_theme()
        
        # 创建UI组件
        self.menu_bar = AppMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # 初始化语言菜单
        from src.localization import get_available_languages, get_current_language
        languages = get_available_languages()
        current_lang = get_current_language()
        self.menu_bar.populate_language_menu(languages, current_lang)
        
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
        self.ui_state_manager.image_state_changed.connect(lambda has_image: 
            self.menu_bar.update_menu_states(has_image, False, False, False))
        self.ui_state_manager.image_state_changed.connect(self.status_bar.update_status)

        self.ui_state_manager.history_state_changed.connect(lambda can_undo, can_redo: 
            self.control_panel.update_button_states(self.ui_state_manager.get_image_state(), can_undo, can_redo))
        self.ui_state_manager.history_state_changed.connect(lambda can_undo, can_redo:
            self.menu_bar.update_menu_states(self.ui_state_manager.get_image_state(), can_undo, can_redo, self.ui_state_manager.get_selection_state()))
        self.ui_state_manager.history_state_changed.connect(lambda can_undo, can_redo:
            self.status_bar.update_status(self.ui_state_manager.get_image_state(), can_undo, can_redo))

        self.ui_state_manager.selection_state_changed.connect(lambda has_selection:
            self.menu_bar.update_menu_states(self.ui_state_manager.get_image_state(), 
                                           self.ui_state_manager.get_history_state()[0], 
                                           self.ui_state_manager.get_history_state()[1], 
                                           has_selection))
        
        # 连接控制面板的用户操作到业务逻辑
        self.control_panel.open_image_clicked.connect(self.handle_open_image)
        self.control_panel.save_image_clicked.connect(self.handle_save_image)
        self.control_panel.undo_clicked.connect(self.handle_undo)
        self.control_panel.redo_clicked.connect(self.handle_redo)
        self.control_panel.clear_clicked.connect(self.handle_clear_selection)
        self.control_panel.clear_image_clicked.connect(self.handle_clear_image)
        self.control_panel.apply_mosaic_clicked.connect(self.handle_apply_mosaic)
        self.control_panel.block_size_changed.connect(self.ui_state_manager.set_block_size)
        self.control_panel.intensity_changed.connect(self.ui_state_manager.set_intensity)
        
        # 连接菜单栏的用户操作
        self.menu_bar.open_image_triggered.connect(self.handle_open_image)
        self.menu_bar.save_image_triggered.connect(self.handle_save_image)
        self.menu_bar.undo_triggered.connect(self.handle_undo)
        self.menu_bar.redo_triggered.connect(self.handle_redo)
        self.menu_bar.clear_triggered.connect(self.handle_clear_selection)
        self.menu_bar.apply_mosaic_triggered.connect(self.handle_apply_mosaic)
        self.menu_bar.language_changed.connect(self.handle_language_change)
        self.menu_bar.theme_settings_triggered.connect(self.show_theme_settings)
        self.menu_bar.about_triggered.connect(self.show_about)
        self.menu_bar.exit_triggered.connect(self.close)
        
        # 连接文件管理器的信号
        self.file_manager.image_opened.connect(self.on_image_opened)
        
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
        from src.gui.about_dialog import show_about_dialog
        show_about_dialog(self)
    
    def show_theme_settings(self):
        """显示主题设置对话框"""
        from src.gui.theme_manager import get_theme_manager
        
        theme_manager = get_theme_manager()
        available_themes = theme_manager.get_available_themes()
        current_theme = theme_manager.get_current_theme()
        
        # 创建简单的主题选择对话框
        dialog = QMessageBox(self)
        dialog.setWindowTitle(tr('theme_settings', 'Theme Settings'))
        dialog.setText(tr('select_theme', 'Select theme:'))
        
        # 添加主题选项按钮
        buttons = []
        for theme_key, theme_name in available_themes.items():
            button = dialog.addButton(theme_name, QMessageBox.AcceptRole)
            buttons.append((button, theme_key))
            if theme_key == current_theme:
                dialog.setDefaultButton(button)
        
        dialog.addButton(QMessageBox.Cancel)
        dialog.exec()
        
        # 获取选中的按钮
        clicked_button = dialog.clickedButton()
        for button, theme_key in buttons:
            if clicked_button == button:
                theme_manager.set_theme(theme_key)
                break
    
    def handle_open_image(self):
        """处理打开图像 - 使用FileManager"""
        self.file_manager.open_image_file()
    
    def on_image_opened(self, image, file_path):
        """处理图像打开完成 - 加载到图像查看器"""
        self.image_viewer.load_image(file_path)
        
    def handle_save_image(self):
        """处理保存图像 - 使用FileManager"""
        current_image = self.image_viewer.get_current_image()
        if current_image:
            self.file_manager.save_image_file(current_image, self)
        else:
            QMessageBox.warning(self, tr("warning"), tr("no_image_to_save"))
        
    def handle_undo(self):
        """处理撤销 - 使用EditHistory"""
        previous_image = self.history.undo()
        if previous_image:
            self.image_viewer.update_image(previous_image)
            # 更新UI状态
            self.ui_state_manager.set_history_state(self.history.can_undo(), self.history.can_redo())
            self.control_panel.update_button_states(
                has_image=self.image_viewer.has_image(),
                can_undo=self.history.can_undo(),
                can_redo=self.history.can_redo(),
                has_selection=False
            )
            self.menu_bar.update_menu_states(
                has_image=self.image_viewer.has_image(),
                can_undo=self.history.can_undo(),
                can_redo=self.history.can_redo(),
                has_selection=False
            )
            self.status_bar.update_status(
                has_image=self.image_viewer.has_image(),
                can_undo=self.history.can_undo(),
                can_redo=self.history.can_redo()
            )
        
    def handle_redo(self):
        """处理重做 - 使用EditHistory"""
        next_image = self.history.redo()
        if next_image:
            self.image_viewer.update_image(next_image)
            # 更新UI状态
            self.ui_state_manager.set_history_state(self.history.can_undo(), self.history.can_redo())
            self.control_panel.update_button_states(
                has_image=self.image_viewer.has_image(),
                can_undo=self.history.can_undo(),
                can_redo=self.history.can_redo(),
                has_selection=False
            )
            self.menu_bar.update_menu_states(
                has_image=self.image_viewer.has_image(),
                can_undo=self.history.can_undo(),
                can_redo=self.history.can_redo(),
                has_selection=False
            )
            self.status_bar.update_status(
                has_image=self.image_viewer.has_image(),
                can_undo=self.history.can_undo(),
                can_redo=self.history.can_redo()
            )
        
    def handle_clear_selection(self):
        """处理清除选择 - 使用ImageViewer"""
        self.image_viewer.clear_selection()
    
    def handle_clear_image(self):
        """处理清除图像 - 清空当前图片"""
        # 清除图像查看器中的图像
        self.image_viewer.clear_image()
        
        # 重置历史记录
        self.history.clear()
        
        # 更新UI状态
        self.ui_state_manager.set_image_state(False)
        self.ui_state_manager.set_history_state(False, False)
        self.ui_state_manager.set_selection_state(False)
        
        # 显示清除完成消息
        self.status_bar.show_message(tr('image_cleared', "Image cleared"))
    
    def handle_apply_mosaic(self):
        """处理应用马赛克 - 使用ImageMosaic功能"""
        if not self.image_viewer.has_image():
            QMessageBox.warning(self, tr("warning"), tr("no_image_loaded"))
            return
        
        selection_rect = self.image_viewer.get_selection_rect()
        if not selection_rect or not selection_rect.isValid():
            QMessageBox.warning(self, tr("warning"), tr("select_area_first"))
            return
        
        try:
            from src.features.image_mosaic import apply_mosaic
            current_image = self.image_viewer.get_current_image()
            block_size = self.control_panel.get_block_size()
            
            # 应用马赛克
            intensity = self.control_panel.get_intensity() / 10.0  # 将1-10转换为0.0-1.0
            processed_image = apply_mosaic(current_image, selection_rect, block_size, intensity)
            
            # 更新显示
            self.image_viewer.update_image(processed_image)
            
            # 添加到历史记录
            self.history.add_state(processed_image.copy())
            
            # 更新历史状态
            self.ui_state_manager.set_history_state(self.history.can_undo(), self.history.can_redo())
            
            # 清除选择
            self.image_viewer.clear_selection()
            
            # 显示完成消息
            self.status_bar.show_mosaic_applied()
            
        except Exception as e:
            QMessageBox.critical(self, tr("error"), f"{tr('apply_mosaic_failed')}: {str(e)}")
    
    def on_block_size_changed(self, value):
        """块大小改变处理"""
        self.block_size = value
        self.ui_state_manager.set_block_size(value)
        self.status_bar.show_message(tr('block_size_changed').format(value))
    
    def handle_language_change(self, language_code):
        """处理语言切换 - 使用Translator类"""
        self.change_language(language_code)
    
    def handle_selection_made(self, rect):
        """处理选择区域 - 使用UIStateManager和ImageViewer"""
        self.ui_state_manager.set_selection_state(True)
        # 更新应用马赛克按钮状态
        self.control_panel.update_button_states(
            has_image=self.image_viewer.has_image(),
            can_undo=self.history.can_undo(),
            can_redo=self.history.can_redo(),
            has_selection=rect.isValid() if rect else False
        )
        
    def handle_image_loaded(self, image_path):
        """处理图像加载 - 使用UIStateManager"""
        # 将当前图像添加到历史记录
        current_image = self.image_viewer.get_current_image()
        if current_image:
            self.history.add_state(current_image.copy())
        
        self.ui_state_manager.set_image_state(True)
        # 重置选择状态并更新历史记录状态
        self.ui_state_manager.set_history_state(self.history.can_undo(), self.history.can_redo())
        # 显示加载完成消息
        self.status_bar.show_image_loaded()
    
    def change_language(self, language_code):
        """切换语言 - 使用Translator类"""
        if set_language(language_code):
            # 保存语言配置
            from main import save_language_config
            save_language_config(language_code)
            # 重新翻译UI
            self.retranslate_ui()
    
    def retranslate_ui(self):
        """重新翻译UI - 使用Translator类"""
        self.setWindowTitle(tr('app_name'))
        
        # 重新翻译菜单栏
        self.menu_bar.retranslate_ui()
        
        # 重新翻译控制面板
        self.control_panel.retranslate_ui()
        
        # 重新翻译状态栏
        self.status_bar.retranslate_ui()
        
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