# -*-coding:utf-8-*-
import ttkbootstrap as ttk


class NodeTreeview(ttk.Treeview):

    def __init__(self, master, bscrollx=True, bscrolly=True):
        super().__init__(master)
        if bscrollx:
            self.with_scrollx()
        if bscrolly:
            self.with_scrolly()

    def delete_all(self):
        for i in self.get_children():
            self.delete(i)

    def with_scrollx(self):
        scrollbar_h = ttk.Scrollbar(self, orient=ttk.HORIZONTAL)
        scrollbar_h.pack(side=ttk.BOTTOM, fill=ttk.X)
        self['xscrollcommand'] = scrollbar_h.set
        scrollbar_h.config(command=self.xview)  # 水平滚动条绑定text

    def with_scrolly(self):
        scrollbar_v = ttk.Scrollbar(self, orient=ttk.VERTICAL)
        scrollbar_v.pack(side=ttk.RIGHT, fill=ttk.Y)
        self['yscrollcommand'] = scrollbar_v.set
        scrollbar_v.config(command=self.yview)  # 垂直滚动条绑定text
