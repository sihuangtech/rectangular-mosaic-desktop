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
APP_NAME = "矩形马赛克"
ORGANIZATION_NAME = "彩旗工作室"
APP_VERSION = "0.1.0"

# Mac平台专用包名（Bundle Identifier）
MAC_PACKAGE_NAME = "cn.skstudio.rectmosaic.mac"
