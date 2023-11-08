import ttkbootstrap as ttk

from gui.converterFrame.timestampFrame import TimestampFrame
from gui.converterFrame.vin9Frame import Vin9Frame


class FunctionFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        # 初始化界面
        group = ttk.LabelFrame(self, text="时间转换器", padding=2)
        self.time_frame = TimestampFrame(group)
        group.pack(side=ttk.LEFT, expand=1)

        group = ttk.LabelFrame(self, text="车架号生成器", padding=2)
        self.time_frame = Vin9Frame(group)
        group.pack(side=ttk.RIGHT, expand=1)