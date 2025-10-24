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
        self.translations = {}
        self.qt_translator = QTranslator()
        self.translations_dir = Path(__file__).parent / 'translations'
        self.load_translations()
        # 根据系统语言设置默认语言
        self.current_language = self.get_system_language()
    
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
    
    def get_system_language(self):
        """获取系统语言，如果系统语言不在支持列表中则返回英文"""
        import platform
        system = platform.system()
        
        if system == 'Darwin':  # macOS
            return self._get_macos_language()
        elif system == 'Windows':
            return self._get_windows_language()
        else:  # Linux或其他系统
            return self._get_linux_language()
    
    def _get_macos_language(self):
        """获取macOS系统语言"""
        try:
            import subprocess
            import os
            # 添加CREATE_NO_WINDOW标志防止控制台弹出
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(['defaults', 'read', '-g', 'AppleLanguages'], 
                                  capture_output=True, text=True, timeout=5, startupinfo=startupinfo)
            if result.returncode == 0 and result.stdout:
                import re
                lang_match = re.search(r'"([^"]+)"', result.stdout)
                if lang_match:
                    apple_lang = lang_match.group(1)
                    # 转换Apple语言格式到我们的格式
                    if 'zh' in apple_lang:
                        return 'zh-CN'
                    elif 'ja' in apple_lang:
                        return 'ja-JP'
                    elif 'ko' in apple_lang:
                        return 'ko-KR'
                    elif 'fr' in apple_lang:
                        return 'fr-FR'
                    elif 'de' in apple_lang:
                        return 'de-DE'
                    elif 'es' in apple_lang:
                        return 'es-ES'
                    elif 'ru' in apple_lang:
                        return 'ru-RU'
        except Exception:
            pass
        return 'en-US'
    
    def _get_windows_language(self):
        """获取Windows系统语言"""
        try:
            import subprocess
            import os
            # 使用PowerShell获取系统UI语言，添加CREATE_NO_WINDOW标志防止控制台弹出
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run([
                'powershell', '-Command', 
                'Get-WinSystemLocale | Select-Object -ExpandProperty Name'
            ], capture_output=True, text=True, timeout=5, startupinfo=startupinfo)
            
            if result.returncode == 0 and result.stdout.strip():
                win_lang = result.stdout.strip()
                # Windows语言格式映射
                lang_map = {
                    'zh-CN': 'zh-CN', 'zh-Hans-CN': 'zh-CN',
                    'ja-JP': 'ja-JP', 'ko-KR': 'ko-KR',
                    'fr-FR': 'fr-FR', 'de-DE': 'de-DE',
                    'es-ES': 'es-ES', 'ru-RU': 'ru-RU',
                    'en-US': 'en-US', 'en-GB': 'en-US'
                }
                if win_lang in lang_map:
                    return lang_map[win_lang]
                
                # 如果完整匹配失败，尝试简写匹配
                lang_prefix = win_lang.split('-')[0]
                if lang_prefix == 'zh':
                    return 'zh-CN'
                elif lang_prefix == 'ja':
                    return 'ja-JP'
                elif lang_prefix == 'ko':
                    return 'ko-KR'
                elif lang_prefix == 'fr':
                    return 'fr-FR'
                elif lang_prefix == 'de':
                    return 'de-DE'
                elif lang_prefix == 'es':
                    return 'es-ES'
                elif lang_prefix == 'ru':
                    return 'ru-RU'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return 'en-US'
    
    def _get_linux_language(self):
        """获取Linux系统语言"""
        try:
            import subprocess
            import os
            # 添加CREATE_NO_WINDOW标志防止控制台弹出
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(['locale'], capture_output=True, text=True, timeout=5, startupinfo=startupinfo)
            if result.returncode == 0 and result.stdout:
                for line in result.stdout.split('\n'):
                    if line.startswith('LANG='):
                        lang = line.split('=')[1].strip().replace('"', '')
                        lang_prefix = lang.split('_')[0]
                        if lang_prefix == 'zh':
                            return 'zh-CN'
                        elif lang_prefix == 'ja':
                            return 'ja-JP'
                        elif lang_prefix == 'ko':
                            return 'ko-KR'
                        elif lang_prefix == 'fr':
                            return 'fr-FR'
                        elif lang_prefix == 'de':
                            return 'de-DE'
                        elif lang_prefix == 'es':
                            return 'es-ES'
                        elif lang_prefix == 'ru':
                            return 'ru-RU'
                        break
        except Exception:
            pass
        return 'en-US'

# 全局翻译器实例
translator = Translator()

# 语言配置常量
LANGUAGES = {
    'zh-CN': {'name': '中文', 'english_name': 'Chinese', 'flag': '🇨🇳'},
    'en-US': {'name': 'English', 'english_name': 'English', 'flag': '🇺🇸'},
    'ja-JP': {'name': '日本語', 'english_name': 'Japanese', 'flag': '🇯🇵'},
    'ko-KR': {'name': '한국어', 'english_name': 'Korean', 'flag': '🇰🇷'},
    'fr-FR': {'name': 'Français', 'english_name': 'French', 'flag': '🇫🇷'},
    'de-DE': {'name': 'Deutsch', 'english_name': 'German', 'flag': '🇩🇪'},
    'es-ES': {'name': 'Español', 'english_name': 'Spanish', 'flag': '🇪🇸'},
    'ru-RU': {'name': 'Русский', 'english_name': 'Russian', 'flag': '🇷🇺'}
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