# -*-coding:utf-8-*-
import ttkbootstrap as ttk
from gui.control.tree.nodeTreeview import NodeTreeview


class JsonTreeview(NodeTreeview):

    def __init__(self, master):
        super().__init__(master)
        self.column("#0", width=100)
        self.heading("#0", text="Name")
        self["columns"] = ("value")
        self.column("value", width=150)
        self.heading("value", text="Value")

    def insert_node(self, parent, k, v):
        if isinstance(v, str):
            return self.insert(parent, ttk.END, text=k, values=(v,), open=True)
        else:
            return self.insert(parent, ttk.END, text=k, open=True)

    def load_tree(self, parent, obj):
        global root
        if parent == '':
            root = self.insert(parent, ttk.END, text="[]", values=("",), open=True)
        if isinstance(obj, list):
            for p in obj:
                parent = self.insert(root, ttk.END, text="{}", values=("",), open=True)
                if isinstance(p, dict):
                    self._load(parent, p)
        elif isinstance(obj, dict):
            self._load(parent, obj)

    def _load(self, parent, obj):
        for k, v in obj.items():
            item = self.insert_node(parent, k, v)
            self.load_tree(item, v)
