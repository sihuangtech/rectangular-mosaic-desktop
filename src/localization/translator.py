# -*- coding: utf-8 -*-
"""
Translator module for Rectangular Mosaic Desktop

用途：
    提供翻译功能，支持动态语言切换。

使用场景：
    被主程序和各模块导入使用，实现界面国际化。
"""

import json
from pathlib import Path
from PySide6.QtCore import QTranslator, QCoreApplication

class Translator:
    """翻译器类，管理应用程序的多语言支持"""
    
    def __init__(self):
        self.current_language = 'en-US'  # 默认语言
        self.translations = {}
        self.qt_translator = QTranslator()
        self.translations_dir = Path(__file__).parent / 'translations'
        self.load_translations()
    
    def load_translations(self):
        """从JSON文件加载翻译数据"""
        self.translations = {}
        
        # 获取所有JSON翻译文件
        if self.translations_dir.exists():
            for json_file in self.translations_dir.glob('*.json'):
                lang_code = json_file.stem
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Failed to load translation file {json_file}: {e}")
        
        # 如果没有找到任何翻译文件，使用默认的空翻译
        if not self.translations:
            self.translations['en-US'] = {}
    
    def set_language(self, language_code):
        """设置当前语言"""
        if language_code in self.translations:
            self.current_language = language_code
            # 加载 Qt 自带的翻译文件（如果有）
            self._load_qt_translations(language_code)
            return True
        return False
    
    def _load_qt_translations(self, language_code):
        """加载 Qt 框架的翻译文件"""
        # 移除旧的翻译器
        QCoreApplication.removeTranslator(self.qt_translator)
        
        # 加载 Qt 自带的翻译文件
        qt_translator = QTranslator()
        if qt_translator.load(f"qt_{language_code}"):
            QCoreApplication.installTranslator(qt_translator)
            self.qt_translator = qt_translator
    
    def get_text(self, key, default=None):
        """获取翻译文本"""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, default or key)
        return default or key
    
    def get_current_language_name(self):
        """获取当前语言的显示名称"""
        if self.current_language in LANGUAGES:
            return LANGUAGES[self.current_language]['name']
        return "Unknown"
    
    def get_current_language_english_name(self):
        """获取当前语言的英文名称"""
        if self.current_language in LANGUAGES:
            return LANGUAGES[self.current_language]['english_name']
        return "Unknown"
    
    def get_available_languages(self):
        """获取可用的语言列表，返回排序后的语言代码列表"""
        return sorted(list(self.translations.keys()))

# 全局翻译器实例
translator = Translator()

# 语言配置常量
LANGUAGES = {
    'zh_CN': {'name': '中文', 'english_name': 'Chinese', 'flag': '🇨🇳'},
    'en_US': {'name': 'English', 'english_name': 'English', 'flag': '🇺🇸'},
    'ja_JP': {'name': '日本語', 'english_name': 'Japanese', 'flag': '🇯🇵'},
    'ko_KR': {'name': '한국어', 'english_name': 'Korean', 'flag': '🇰🇷'},
    'fr_FR': {'name': 'Français', 'english_name': 'French', 'flag': '🇫🇷'},
    'de_DE': {'name': 'Deutsch', 'english_name': 'German', 'flag': '🇩🇪'},
    'es_ES': {'name': 'Español', 'english_name': 'Spanish', 'flag': '🇪🇸'},
    'ru_RU': {'name': 'Русский', 'english_name': 'Russian', 'flag': '🇷🇺'}
}

def tr(key, default=None):
    """翻译函数，简化翻译调用"""
    return translator.get_text(key, default)

def get_available_languages():
    """获取可用语言列表"""
    return translator.get_available_languages()

def set_language(language_code):
    """设置当前语言"""
    return translator.set_language(language_code)

def get_current_language():
    """获取当前语言代码"""
    return translator.current_language