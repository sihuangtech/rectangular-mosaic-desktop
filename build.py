#!/usr/bin/env python3
"""
矩形马赛克应用构建脚本

这是一个简化的入口脚本，实际的构建逻辑在 src/builder/ 模块中。

使用方法:
    python build.py

功能:
- 支持多平台打包 (Windows, macOS, Linux)
- 支持多种架构 (x86_64, arm64)
- 支持多种输出格式 (.exe, .app, .dmg, .pkg, .deb, .rpm)
- 支持 Mac App Store 专用打包
- 交互式配置界面
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.builder.main_builder import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"导入构建模块失败: {e}")
    print("请确保项目结构完整，src/builder/ 目录存在")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n\n用户中断构建")
    sys.exit(1)
except Exception as e:
    print(f"构建过程中出错: {e}")
    sys.exit(1)