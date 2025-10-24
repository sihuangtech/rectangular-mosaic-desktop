# -*- coding: utf-8 -*-
"""
菜单栏组件模块 - 包含应用程序的菜单栏
"""
from PySide6.QtWidgets import QMenuBar, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QKeySequence, QAction
from src.localization import tr


class AppMenuBar(QMenuBar):
    """应用程序菜单栏"""
    
    # 信号定义
    open_image_triggered = Signal()
    save_image_triggered = Signal()
    undo_triggered = Signal()
    redo_triggered = Signal()
    clear_triggered = Signal()
    language_changed = Signal(str)
    about_triggered = Signal()
    exit_triggered = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menus()
    
    def init_menus(self):
        """初始化菜单"""
        # 文件菜单
        self.create_file_menu()
        
        # 编辑菜单
        self.create_edit_menu()
        
        # 视图菜单
        self.create_view_menu()
        
        # 工具菜单
        self.create_tools_menu()
        
        # 帮助菜单
        self.create_help_menu()
    
    def create_file_menu(self):
        """创建文件菜单"""
        file_menu = self.addMenu(tr("file", "File"))
        
        # 打开图片
        open_action = QAction(tr("open_image", "Open Image"), self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_image_triggered.emit)
        file_menu.addAction(open_action)
        
        # 保存图片
        save_action = QAction(tr("save_image", "Save Image"), self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_image_triggered.emit)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction(tr("exit", "Exit"), self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.exit_triggered.emit)
        file_menu.addAction(exit_action)
        
        # 保存引用以便后续更新状态
        self.open_action = open_action
        self.save_action = save_action
    
    def create_edit_menu(self):
        """创建编辑菜单"""
        edit_menu = self.addMenu(tr("edit", "Edit"))
        
        # 撤销
        undo_action = QAction(tr("undo", "Undo"), self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo_triggered.emit)
        edit_menu.addAction(undo_action)
        
        # 重做
        redo_action = QAction(tr("redo", "Redo"), self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.redo_triggered.emit)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # 清除
        clear_action = QAction(tr("clear", "Clear"), self)
        clear_action.triggered.connect(self.clear_triggered.emit)
        edit_menu.addAction(clear_action)
        
        # 保存引用以便后续更新状态
        self.undo_action = undo_action
        self.redo_action = redo_action
        self.clear_action = clear_action
    
    def create_view_menu(self):
        """创建视图菜单"""
        view_menu = self.addMenu(tr("view", "View"))
        
        # 这里可以添加视图相关的菜单项
        # 例如：缩放、全屏等
        
        self.view_menu = view_menu
    
    def create_tools_menu(self):
        """创建工具菜单"""
        tools_menu = self.addMenu(tr("tools", "Tools"))
        
        # 语言子菜单
        language_menu = tools_menu.addMenu(tr("language", "Language"))
        self.language_menu = language_menu
        
        # 设置子菜单
        settings_menu = tools_menu.addMenu(tr("settings", "Settings"))
        self.settings_menu = settings_menu
        
        self.tools_menu = tools_menu
    
    def create_help_menu(self):
        """创建帮助菜单"""
        help_menu = self.addMenu(tr("help", "Help"))
        
        # 关于
        about_action = QAction(tr("about", "About"), self)
        about_action.triggered.connect(self.about_triggered.emit)
        help_menu.addAction(about_action)
        
        self.help_menu = help_menu
    
    def update_menu_states(self, has_image=False, can_undo=False, can_redo=False):
        """更新菜单项状态"""
        self.open_action.setEnabled(True)  # 总是可以打开
        self.save_action.setEnabled(has_image)
        self.undo_action.setEnabled(can_undo)
        self.redo_action.setEnabled(can_redo)
        self.clear_action.setEnabled(has_image)
    
    def populate_language_menu(self, languages, current_language):
        """填充语言菜单"""
        self.language_menu.clear()
        
        for lang_code in languages:
            action = QAction(lang_code, self)
            action.setCheckable(True)
            action.setChecked(lang_code == current_language)
            action.triggered.connect(lambda checked, code=lang_code: self.language_changed.emit(code))
            self.language_menu.addAction(action)
    