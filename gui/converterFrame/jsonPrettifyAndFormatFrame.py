import ttkbootstrap as ttk
import utils.jsonUtils as jsonUtils
import json

from gui.control.tree.jsonTreeview import JsonTreeview
from gui.control.text.popmenuText import PopMenuText


class JSONPrettifyAndFormatFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.init_top_frame()
        self.init_left_frame()
        self.init_right_frame()

    def init_top_frame(self):
        topframe = ttk.Frame(self)
        t1 = ttk.Frame(topframe)

        t2 = ttk.Frame(t1)
        self.indent_label = ttk.Label(t2, text='缩进空格数:')
        self.indent_label.pack(side=ttk.LEFT, expand=True)

        self.spinbox = ttk.Spinbox(master=t2, from_=1, to=10, width=2, )
        self.spinbox.pack(side=ttk.LEFT, expand=True)
        self.spinbox.set(4)
        self.spinbox.config(state='readonly')

        t2.pack(side=ttk.LEFT, expand=True)

        # clear
        self.clear_button = ttk.Button(t1, bootstyle=ttk.PRIMARY, text='清空')
        self.clear_button.pack(side=ttk.LEFT, expand=True)
        self.clear_button.configure(command=self.jons_clear)

        # format
        self.format_button = ttk.Button(t1, bootstyle=ttk.WARNING, text='格式化')
        self.format_button.pack(side=ttk.LEFT, expand=True)
        self.format_button.configure(command=self.jons_format)

        self.compress_button = ttk.Button(t1, bootstyle=ttk.DEFAULT, text='压缩')
        self.compress_button.pack(side=ttk.LEFT, expand=True)
        self.compress_button.configure(command=self.json_compress)

        self.escape_button = ttk.Button(t1, bootstyle=ttk.SUCCESS, text='转义')
        self.escape_button.pack(side=ttk.LEFT, expand=True)
        self.escape_button.configure(command=self.json_escape)

        self.unEscape_button = ttk.Button(t1, bootstyle=ttk.SUCCESS, text='去转义')
        self.unEscape_button.pack(side=ttk.LEFT, expand=True)
        self.unEscape_button.configure(command=self.jons_unescape)

        self.copy_button = ttk.Button(t1, bootstyle=ttk.DEFAULT, text='复制结果')
        self.copy_button.pack(side=ttk.LEFT, expand=True)
        self.copy_button.configure(command=self.json_copy)

        btn = ttk.Button(t1, bootstyle=ttk.LIGHT, text='1212')
        btn.pack(side=ttk.LEFT, expand=True)

        t1.pack(fill=ttk.BOTH, expand=ttk.YES)
        topframe.pack(fill=ttk.BOTH, expand=ttk.YES)

    def init_left_frame(self):
        leftframe = ttk.Frame(self)

        self.origin_text = PopMenuText(leftframe, padding=5, width=60, height=60, autohide=True, vbar=True)
        self.origin_text.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=ttk.YES)
        self.origin_text.focus_set()

        self.format_text = PopMenuText(leftframe, width=60, padding=5, autohide=True, vbar=True, hbar=True)
        self.format_text.pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=ttk.YES)

        leftframe.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=True)

    def init_right_frame(self):
        rightframe = ttk.Frame(self)

        self.treeView = JsonTreeview(rightframe)
        self.treeView.pack(fill=ttk.BOTH, expand=1)

        rightframe.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=ttk.YES, )

    def json_escape(self):
        # format ..Escape
        json_text = self.origin_text.get(1.0, ttk.END)
        if json_text:
            if jsonUtils.is_json(json_text):
                self.format_text.delete(1.0, ttk.END)
                self.format_text.insert(1.0, jsonUtils.escape(json_text, int(self.spinbox.get())))

    def jons_format(self):
        json_text = self.origin_text.get(1.0, ttk.END)
        if json_text and len(json_text) > 0 and json_text != '\n':
            if jsonUtils.is_json(json_text):
                self.format_text.delete(1.0, ttk.END)
                format = jsonUtils.format(json_text, int(self.spinbox.get()))
                self.format_text.insert(1.0, format)
                self.treeView.delete_all()
                try:
                    if jsonUtils.is_json(format):
                        self.treeView.load_tree('', json.loads(format))
                except Exception as e:
                    return

    def json_compress(self):
        json_text = self.origin_text.get(1.0, ttk.END)
        if json_text:
            if jsonUtils.is_json(json_text):
                self.format_text.delete(1.0, ttk.END)
                self.format_text.insert(1.0, jsonUtils.compress(json_text))

    def jons_clear(self):
        self.format_text.new()
        self.origin_text.new()
        self.treeView.delete_all()

    def json_copy(self):
        # 剪切板
        import pyperclip
        pyperclip.copy(self.format_text.get(1.0, ttk.END))

    def jons_unescape(self):
        json_text = self.origin_text.get(1.0, ttk.END)
        if json_text:
            self.format_text.delete(1.0, ttk.END)
            self.format_text.insert(1.0, jsonUtils.unescape(json_text, int(self.spinbox.get())))
