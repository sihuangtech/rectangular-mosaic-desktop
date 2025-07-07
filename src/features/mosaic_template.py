# -*- coding: utf-8 -*-
"""
马赛克模板功能模块

用途：
    提供马赛克模板的保存、加载、应用等功能。
    模板支持多个矩形区域，按图片比例存储，适配不同尺寸图片。

使用场景：
    被主界面调用，实现批量自动马赛克。
"""
import json
from typing import List, Dict

class MosaicTemplate:
    """
    马赛克模板类，保存一组矩形区域的比例信息。
    """
    def __init__(self, rects: List[Dict[str, float]] = None):
        """
        参数：
            rects (List[Dict]): 每个字典包含 x, y, w, h（均为0~1比例）
        """
        self.rects = rects or []

    def add_rect(self, x: float, y: float, w: float, h: float):
        """
        添加一个矩形区域。
        参数：
            x, y, w, h (float): 左上角和宽高比例（0~1）
        """
        self.rects.append({'x': x, 'y': y, 'w': w, 'h': h})

    def clear(self):
        """
        清空所有区域。
        """
        self.rects.clear()

    def save_to_file(self, file_path: str):
        """
        保存模板到 JSON 文件。
        参数：
            file_path (str): 文件路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'rects': self.rects}, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_from_file(file_path: str) -> 'MosaicTemplate':
        """
        从 JSON 文件加载模板。
        参数：
            file_path (str): 文件路径
        返回：
            MosaicTemplate: 加载的模板对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return MosaicTemplate(rects=data.get('rects', []))

    def get_pixel_rects(self, img_width: int, img_height: int) -> List[Dict[str, int]]:
        """
        按图片尺寸换算所有区域的像素坐标。
        参数：
            img_width (int): 图片宽度
            img_height (int): 图片高度
        返回：
            List[Dict]: 每个字典包含 x, y, w, h（像素值）
        """
        result = []
        for r in self.rects:
            x = int(r['x'] * img_width)
            y = int(r['y'] * img_height)
            w = int(r['w'] * img_width)
            h = int(r['h'] * img_height)
            result.append({'x': x, 'y': y, 'w': w, 'h': h})
        return result 