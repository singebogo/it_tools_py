import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.control.searchDialog import SearchDialog
from utils.charsetUtils import to_bytes, handle, bell_


class ReplaceDialog(SearchDialog):
    
    def __init__(self, master, **kw):
        super(ReplaceDialog, self).__init__(master=master, **kw)

    # 替换对话框
    def show(self):
        self.init_window(title="替换")
        frame = ttk.Frame(self)
        ttk.Button(frame, text="查找下一个", command=self._findnext).pack(pady=2)
        ttk.Button(frame, text="替换", command=self.replace).pack(padx=2, pady=2)
        ttk.Button(frame, text="全部替换", command=self.replace_all).pack(padx=2, pady=2)
        frame.pack(side=RIGHT, fill=Y, pady=2)

        inputbox = ttk.Frame(self)
        ttk.Label(inputbox, text="查找内容:").pack(side=LEFT, pady=2)
        self.keyword = ttk.StringVar(self.master)
        keyword = ttk.Entry(inputbox, textvariable=self.keyword)
        keyword.pack(side=LEFT, expand=True, fill=X, padx=2, pady=2)
        keyword.focus_force()
        inputbox.pack(fill=X, padx=2, pady=2)

        replace = ttk.Frame(self)
        ttk.Label(replace, text="替换为:  ").pack(side=LEFT)
        self.text_to_replace = ttk.StringVar(self.master)
        replace_text = ttk.Entry(replace, textvariable=self.text_to_replace)
        replace_text.pack(side=LEFT, expand=True, fill=X, padx=2, pady=2)
        replace_text.bind("<Key-Return>", self.replace)
        replace.pack(fill=X, padx=2, pady=2)

        options = ttk.Frame(self)
        self.create_options(options)
        options.pack(fill=X, padx=2, pady=2)

    def _findnext(self):  # 仅用于"查找下一个"按钮功能
        text = self.master.text
        sel_range = text.tag_ranges('sel')  # 获得选区的起点和终点
        if sel_range:
            selectarea = sel_range[0].string, sel_range[1].string
            result = self.findnext('start')
            if result is None: return
            if result[0] == selectarea[0]:  # 若仍停留在原位置
                text.mark_set('insert', result[1])  # 从选区终点继续查找
                self.findnext('start')
        else:
            self.findnext('start')

    def wm_title(self, string=None):
        """Set the title of this widget."""
        return self.tk.call('wm', 'title', self._w, string)

    def replace(self, bell=True, mark=True):
        text = self.master.text
        result = self.search(mark=False, bell=bell)
        if not result:
            return  # 标志已无文本可替换

        self.master.show_line()
        pos, newpos = result
        newtext = self.text_to_replace.get()
        try:
            if self.use_escape_char.get():
                newtext = to_bytes(newtext).decode(self.master.coding.get())
            if self.use_regexpr.get():
                old = text.get(pos, newpos)
                newtext = re.sub(self.keyword.get(), newtext, old)
        except Exception as err:
            handle(err, parent=self)
            return
        text.delete(pos, newpos)
        text.insert(pos, newtext)
        end_pos = "%s+%dc" % (pos, len(newtext))
        if mark: self.mark_text(pos, end_pos)
        return pos, end_pos

    def replace_all(self):
        self.master.text.mark_set("insert", "1.0")
        flag = False  # 标志是否已有文字被替换

        # 以下代码会导致无限替换, 使程序卡死, 新的代码修复了该bug
        # while self.replace(bell=False)!=-1:
        #    flag=True
        last = (0, 0)
        while True:
            result = self.replace(bell=False, mark=False)
            if result is None: break
            flag = True
            result = self.findnext('start', bell=False, mark=False)
            if result is None: return
            ln, col = result[0].split('.')
            ln = int(ln)
            col = int(col)
            # 判断新的偏移量是增加还是减小
            if ln < last[0] or (ln == last[0] and col < last[1]):
                self.mark_text(*result)  # 已完成一轮替换
                break
            last = ln, col
        if not flag: bell_()
