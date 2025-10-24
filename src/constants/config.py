# -*- coding: utf-8 -*-
"""
配置常量模块

用途：
    定义全局使用的常量参数，如马赛克块大小等。

使用场景：
    被各功能模块导入使用。
"""
# 马赛克默认块大小
DEFAULT_MOSAIC_BLOCK_SIZE = 15 
# 块大小可调范围
MIN_MOSAIC_BLOCK_SIZE = 2
MAX_MOSAIC_BLOCK_SIZE = 100 

# 应用元数据
APP_NAME = "Rectangular Mosaic"
ORGANIZATION_NAME = "SK Studio"
APP_VERSION = "0.1.0"
APP_BUILD_NUMBER = "1"

# Mac平台专用包名（Bundle Identifier）
MAC_PACKAGE_NAME = "cn.skstudio.rectmosaic.mac"

# 本地化配置
DEFAULT_LANGUAGE = 'en_US'  # 默认语言
SUPPORTED_LANGUAGES = [
    'zh_CN',  # 简体中文
    'en_US',  # English
    'ja_JP',  # 日本語
    'ko_KR',  # 한국어
    'fr_FR',  # Français
    'de_DE',  # Deutsch
    'es_ES',  # Español
    'ru_RU'   # Русский
]

# 语言配置文件路径
LANGUAGE_CONFIG_FILE = "language_config.json"

# 支持的图像文件扩展名
SUPPORTED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
SUPPORTED_SAVE_EXTENSIONS = ['.png', '.jpg', '.jpeg']

# UI组件配置
UI_CONTROL_PANEL_WIDTH = 250  # 控制面板宽度
UI_BLOCK_SIZE_SPIN_RANGE = (5, 50)  # 块大小微调框范围
UI_BLOCK_SIZE_SLIDER_RANGE = (5, 50)  # 块大小滑块范围
UI_BLOCK_SIZE_DEFAULT = 10  # 块大小默认值
UI_INTENSITY_SPIN_RANGE = (1, 10)  # 强度微调框范围
UI_INTENSITY_SLIDER_RANGE = (1, 10)  # 强度滑块范围
UI_INTENSITY_DEFAULT = 5  # 强度默认值

# 主窗口配置
MAIN_WINDOW_WIDTH = 1000  # 主窗口宽度
MAIN_WINDOW_HEIGHT = 700  # 主窗口高度
MAIN_WINDOW_MIN_WIDTH = 800  # 主窗口最小宽度
MAIN_WINDOW_MIN_HEIGHT = 600  # 主窗口最小高度

# 图像查看器配置
IMAGE_VIEWER_MIN_WIDTH = 400  # 图像查看器最小宽度
IMAGE_VIEWER_MIN_HEIGHT = 300  # 图像查看器最小高度
IMAGE_VIEWER_BACKGROUND_COLOR = "#f0f0f0"  # 图像查看器背景色
IMAGE_VIEWER_BORDER_STYLE = "1px solid #ccc"  # 图像查看器边框样式

# 编辑历史配置
MAX_EDIT_HISTORY = 20  # 最大编辑历史记录数

# 选择工具配置
SELECTION_BORDER_COLOR = (255, 0, 0)  # 选择边框颜色 (RGB)
SELECTION_BORDER_WIDTH = 2  # 选择边框宽度

# UI布局配置
UI_LAYOUT_SPACING = 10  # UI布局间距
UI_LAYOUT_MARGIN = 0  # UI布局边距
