"""
UI状态管理模块 - 管理应用程序的UI状态
"""
from PySide6.QtCore import QObject, Signal
from src.constants.config import UI_BLOCK_SIZE_DEFAULT, UI_INTENSITY_DEFAULT


class UIStateManager(QObject):
    """UI状态管理器类"""
    
    # 状态变化信号
    image_state_changed = Signal(bool)  # 图像加载状态变化
    history_state_changed = Signal(bool, bool)  # 撤销/重做状态变化 (can_undo, can_redo)
    selection_state_changed = Signal(bool)  # 选择状态变化
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.has_image = False
        self.can_undo = False
        self.can_redo = False
        self.has_selection = False
        self.block_size = UI_BLOCK_SIZE_DEFAULT
        self.intensity = UI_INTENSITY_DEFAULT
    
    def set_image_state(self, has_image):
        """设置图像状态"""
        if self.has_image != has_image:
            self.has_image = has_image
            self.image_state_changed.emit(has_image)
    
    def set_history_state(self, can_undo, can_redo):
        """设置历史记录状态"""
        if self.can_undo != can_undo or self.can_redo != can_redo:
            self.can_undo = can_undo
            self.can_redo = can_redo
            self.history_state_changed.emit(can_undo, can_redo)
    
    def set_selection_state(self, has_selection):
        """设置选择状态"""
        if self.has_selection != has_selection:
            self.has_selection = has_selection
            self.selection_state_changed.emit(has_selection)
    
    def set_block_size(self, block_size):
        """设置块大小"""
        self.block_size = block_size
    
    def set_intensity(self, intensity):
        """设置强度"""
        self.intensity = intensity
    
    def get_image_state(self):
        """获取图像状态"""
        return self.has_image
    
    def get_history_state(self):
        """获取历史记录状态"""
        return self.can_undo, self.can_redo
    
    def get_selection_state(self):
        """获取选择状态"""
        return self.has_selection
    
    def get_block_size(self):
        """获取块大小"""
        return self.block_size
    
    def get_intensity(self):
        """获取强度值"""
        return self.intensity
    
    def update_all_states(self, has_image=None, can_undo=None, can_redo=None, has_selection=None):
        """批量更新状态"""
        if has_image is not None:
            self.set_image_state(has_image)
        
        if can_undo is not None and can_redo is not None:
            self.set_history_state(can_undo, can_redo)
        
        if has_selection is not None:
            self.set_selection_state(has_selection)