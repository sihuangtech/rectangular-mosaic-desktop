# -*- coding: utf-8 -*-
"""
菜单栏组件模块 - 包含应用程序的菜单栏
"""
from PySide6.QtWidgets import QMenuBar, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QKeySequence, QAction, QActionGroup
from src.localization import tr
from src.gui.theme_manager import get_theme_manager


class AppMenuBar(QMenuBar):
    """应用程序菜单栏"""
    
    # 信号定义
    open_image_triggered = Signal()
    save_image_triggered = Signal()
    undo_triggered = Signal()
    redo_triggered = Signal()
    clear_triggered = Signal()
    apply_mosaic_triggered = Signal()
    language_changed = Signal(str)
    about_triggered = Signal()
    exit_triggered = Signal()
    theme_settings_triggered = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menus()
    
    def init_menus(self):
        """初始化菜单"""
        # 文件菜单
        self.create_file_menu()
        
        # 编辑菜单
        self.create_edit_menu()
        
        # 设置菜单
        self.create_settings_menu()
        
        # 帮助菜单
        self.create_help_menu()
    
    def retranslate_ui(self):
        """重新翻译UI文本"""
        # 重新翻译所有菜单
        self.clear()
        self.init_menus()
        
        # 重新填充语言菜单（需要重新设置当前语言）
        from src.localization import get_current_language, get_available_languages
        self.populate_language_menu(get_available_languages(), get_current_language())
    
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
        
        # 应用马赛克
        apply_mosaic_action = QAction(tr("apply_mosaic", "Apply Mosaic"), self)
        apply_mosaic_action.triggered.connect(self.apply_mosaic_triggered.emit)
        edit_menu.addAction(apply_mosaic_action)
        
        edit_menu.addSeparator()
        
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
        self.apply_mosaic_action = apply_mosaic_action
    
    def create_settings_menu(self):
        """创建设置菜单"""
        settings_menu = self.addMenu(tr("settings", "Settings"))
        
        # 添加主题选项
        theme_action = QAction(tr("theme", "Theme"), self)
        theme_action.triggered.connect(self.show_theme_settings)
        settings_menu.addAction(theme_action)
        
        # 语言子菜单
        language_menu = settings_menu.addMenu(tr("language", "Language"))
        self.language_menu = language_menu
        
        self.settings_menu = settings_menu
    
    def create_help_menu(self):
        """创建帮助菜单"""
        help_menu = self.addMenu(tr("help", "Help"))
        
        # 关于
        about_action = QAction(tr("about", "About"), self)
        about_action.triggered.connect(self.about_triggered.emit)
        help_menu.addAction(about_action)
        
        self.help_menu = help_menu
    
    def update_menu_states(self, has_image=False, can_undo=False, can_redo=False, has_selection=False):
        """更新菜单项状态"""
        self.open_action.setEnabled(True)  # 总是可以打开
        self.save_action.setEnabled(has_image)
        self.undo_action.setEnabled(can_undo)
        self.redo_action.setEnabled(can_redo)
        self.clear_action.setEnabled(has_image)
        self.apply_mosaic_action.setEnabled(has_image and has_selection)
    
    def populate_language_menu(self, languages, current_language):
        """填充语言菜单"""
        self.language_menu.clear()
        
        # 创建动作组以实现单选
        language_group = QActionGroup(self)
        language_group.setExclusive(True)
        
        for lang_code in languages:
            # 获取语言的本地化名称
            from src.localization import LANGUAGES
            lang_info = LANGUAGES.get(lang_code, {})
            lang_name = lang_info.get('name', lang_code)  # 使用本地化名称，如果没有则使用代码
            
            action = QAction(lang_name, self)
            action.setCheckable(True)
            action.setChecked(lang_code == current_language)
            action.triggered.connect(lambda checked, code=lang_code: self.language_changed.emit(code))
            
            language_group.addAction(action)
            self.language_menu.addAction(action)
    
    def show_theme_settings(self):
        """显示主题设置对话框"""
        self.theme_settings_triggered.emit()


class ThemeSettingsDialog(QDialog):
    """主题设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = get_theme_manager()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(tr("theme_settings", "Theme Settings"))
        self.setModal(True)
        self.resize(300, 200)
        
        # 主布局
        layout = QVBoxLayout(self)
        
        # 主题选项组
        self.theme_group = QButtonGroup(self)
        
        available_themes = self.theme_manager.get_available_themes()
        current_theme = self.theme_manager.get_current_theme()
        
        for theme_key, theme_name in available_themes.items():
            radio = QRadioButton(theme_name)
            radio.setChecked(theme_key == current_theme)
            self.theme_group.addButton(radio, id=self.get_theme_id(theme_key))
            layout.addWidget(radio)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 确定按钮
        ok_button = QPushButton(tr("ok", "OK"))
        ok_button.clicked.connect(self.apply_theme)
        button_layout.addWidget(ok_button)
        
        # 取消按钮
        cancel_button = QPushButton(tr("cancel", "Cancel"))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_theme_id(self, theme_key):
        """获取主题对应的ID"""
        theme_ids = {
            "system": 0,
            "light": 1,
            "dark": 2
        }
        return theme_ids.get(theme_key, 0)
    
    def get_theme_key_from_id(self, theme_id):
        """根据ID获取主题键"""
        theme_keys = ["system", "light", "dark"]
        if 0 <= theme_id < len(theme_keys):
            return theme_keys[theme_id]
        return "system"
    
    def apply_theme(self):
        """应用选择的主题"""
        selected_id = self.theme_group.checkedId()
        theme_key = self.get_theme_key_from_id(selected_id)
        
        if self.theme_manager.set_theme(theme_key):
            self.accept()
        else:
            QMessageBox.warning(self, tr("error", "Error"), 
                              tr("theme_apply_error", "Failed to apply theme"))
    