# -*- coding: utf-8 -*-
"""
批量马赛克处理模块

用途：
    按指定模板对多张图片批量打马赛克，并导出到目标文件夹。

使用场景：
    被主界面调用，实现批量图片自动马赛克。
"""
import os
from typing import List
from PySide6.QtGui import QImage
from src.features.mosaic_template import MosaicTemplate
from src.features.image_mosaic import apply_mosaic

def batch_apply_mosaic(
    image_paths: List[str],
    template: MosaicTemplate,
    output_dir: str,
    block_size: int = 15,
    suffix: str = '_mosaic'
) -> List[str]:
    """
    对多张图片批量应用马赛克模板。
    参数：
        image_paths (List[str]): 待处理图片路径列表
        template (MosaicTemplate): 马赛克模板对象
        output_dir (str): 输出文件夹
        block_size (int): 马赛克块大小
        suffix (str): 输出文件名后缀
    返回：
        List[str]: 处理后图片的输出路径列表
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    result_paths = []
    for img_path in image_paths:
        img = QImage(img_path)
        if img.isNull():
            continue
        w, h = img.width(), img.height()
        for r in template.get_pixel_rects(w, h):
            from PySide6.QtCore import QRect
            rect = QRect(r['x'], r['y'], r['w'], r['h'])
            img = apply_mosaic(img, rect, block_size)
        # 输出文件名
        base = os.path.basename(img_path)
        name, ext = os.path.splitext(base)
        out_path = os.path.join(output_dir, f"{name}{suffix}{ext}")
        img.save(out_path)
        result_paths.append(out_path)
    return result_paths 