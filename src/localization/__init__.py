# -*- coding: utf-8 -*-
"""
Localization module for Rectangular Mosaic Desktop

用途：
    提供多语言支持功能，支持中英日韩法德西俄八种语言。

使用场景：
    被主程序和各模块导入使用，实现界面国际化。
"""

from .translator import Translator, get_available_languages, set_language, get_current_language, tr, LANGUAGES

__all__ = ['Translator', 'get_available_languages', 'set_language', 'get_current_language', 'tr', 'LANGUAGES']