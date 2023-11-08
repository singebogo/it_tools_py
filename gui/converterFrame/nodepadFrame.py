import ttkbootstrap as ttk

from gui.control.text.popmenuText import PopMenuText


class NotepadFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.root = container

        # 初始化界面
        self.text = PopMenuText(self, hbar=False, undo=True)
        self.text.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)
        # 设置焦点
        self.text.focus_set()