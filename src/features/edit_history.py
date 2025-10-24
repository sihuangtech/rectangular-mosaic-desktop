"""
历史管理模块 - 管理图像编辑历史（撤销/重做功能）
"""
from PySide6.QtGui import QImage
from src.constants.config import MAX_EDIT_HISTORY


class EditHistory:
    """编辑历史管理器"""
    
    def __init__(self, max_history=MAX_EDIT_HISTORY):
        """
        初始化编辑历史管理器
        
        Args:
            max_history: 最大历史记录数，默认使用配置值
        """
        self.max_history = max_history
        self.history = []
        self.current_index = -1
    
    def add_state(self, image):
        """添加新的状态到历史记录"""
        if image is None or image.isNull():
            return
        
        # 移除当前索引之后的状态（当用户撤销后进行了新操作时）
        self.history = self.history[:self.current_index + 1]
        
        # 添加新状态
        self.history.append(image.copy())
        self.current_index += 1
        
        # 如果历史记录超过最大限制，移除最老的状态
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1
    
    def can_undo(self):
        """检查是否可以撤销"""
        return self.current_index > 0
    
    def can_redo(self):
        """检查是否可以重做"""
        return self.current_index < len(self.history) - 1
    
    def undo(self):
        """撤销操作"""
        if not self.can_undo():
            return None
        
        self.current_index -= 1
        return self.history[self.current_index].copy()
    
    def redo(self):
        """重做操作"""
        if not self.can_redo():
            return None
        
        self.current_index += 1
        return self.history[self.current_index].copy()
    
    def clear(self):
        """清空历史记录"""
        self.history.clear()
        self.current_index = -1
    
    def get_current_state(self):
        """获取当前状态"""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index].copy()
        return None
    
    def is_empty(self):
        """检查历史记录是否为空"""
        return len(self.history) == 0