import ttkbootstrap as ttk
from tkinter import *
from ttkbootstrap.constants import *
import os
import re

from utils.charsetUtils import to_bytes, handle, bell_


class SearchDialog(Toplevel):
    # 查找对话框
    def __init__(self, master):
        self.master = master
        self.coding = 'utf-8'

    def init_window(self, title="查找"):
        Toplevel.__init__(self, self.master)
        self.title(title)
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        # 当父窗口隐藏后，窗口也跟随父窗口隐藏

        self.transient(self.master)
        self.wm_protocol("WM_DELETE_WINDOW", self.onquit)
        self.attributes("-toolwindow", True)
        self.resizable(False, False)
        self.wm_attributes('-topmost', False)
        self.geometry("+%d+%d" % (self.winfo_screenwidth() / 3, self.winfo_screenheight() / 3))


    def show(self):
        self.init_window()
        frame = Frame(self)
        ttk.Button(frame, text="查找下一个", command=self.search).pack(padx=2, pady=2)
        # ttk.Button(frame, text="退出", command=self.onquit).pack(padx=2, pady=2)
        frame.pack(side=RIGHT, fill=Y)
        inputbox = Frame(self)
        Label(inputbox, text="查找内容:").pack(side=LEFT)
        self.keyword = StringVar(self.master)
        keyword = ttk.Entry(inputbox, textvariable=self.keyword)
        keyword.pack(side=LEFT, expand=True, fill=X, padx=2, pady=2)
        keyword.bind("<Key-Return>", self.search)
        keyword.focus_force()
        inputbox.pack(fill=X, padx=2, pady=2)
        options = Frame(self)
        self.create_options(options)
        options.pack(fill=X)


    def create_options(self, master):
        Label(master, text="选项: ").pack(side=LEFT)
        self.use_regexpr = IntVar(self.master)
        ttk.Checkbutton(master, text="使用正则表达式", variable=self.use_regexpr) \
            .pack(side=LEFT, padx=2, pady=2)
        self.match_case = IntVar(self.master)
        ttk.Checkbutton(master, text="区分大小写", variable=self.match_case) \
            .pack(side=LEFT, padx=2, pady=2)
        self.use_escape_char = IntVar(self.master)
        self.use_escape_char.set(False)
        ttk.Checkbutton(master, text="使用转义字符", variable=self.use_escape_char) \
            .pack(side=LEFT, padx=2, pady=2)

    def search(self, event=None, mark=True, bell=True):
        text = self.master
        key = self.keyword.get()
        if not key: return
        # 验证用户输入是否正常
        if self.use_escape_char.get():
            try:
                key = str(to_bytes(key), encoding=self.coding)
            except Exception as err:
                handle(err, parent=self)
                return
        if self.use_regexpr.get():
            try:
                re.compile(key)
            except re.error as err:
                handle(err, parent=self)
                return
        # 默认从当前光标位置开始查找
        pos = text.search(key, INSERT, 'end-1c',  # end-1c:忽略末尾换行符
                          regexp=self.use_regexpr.get(),
                          nocase=not self.match_case.get())
        if not pos:
            # 尝试从开头循环查找
            pos = text.search(key, '1.0', 'end-1c',
                              regexp=self.use_regexpr.get(),
                              nocase=not self.match_case.get())
        if pos:
            if self.use_regexpr.get():  # 获取正则表达式匹配的字符串长度
                text_after = text.get(pos, END)
                flag = re.IGNORECASE if not self.match_case.get() else 0
                length = re.match(key, text_after, flag).span()[1]
            else:
                length = len(key)
            newpos = "%s+%dc" % (pos, length)
            text.mark_set(INSERT, newpos)
            if mark:
                self.mark_text(pos, newpos)
            return pos, newpos
        elif bell:  # 未找到,返回None
            bell_(widget=self)

    def findnext(self, cursor_pos='end', mark=True, bell=True):
        # cursor_pos:标记文本后将光标放在找到文本开头还是末尾
        # 因为search()默认从当前光标位置开始查找
        # end 用于查找下一个操作, start 用于替换操作
        result = self.search(mark=mark, bell=bell)
        if not result: return
        if cursor_pos == 'end':
            self.master.mark_set('insert', result[1])
        elif cursor_pos == 'start':
            self.master.mark_set('insert', result[0])
        return result

    def mark_text(self, start_pos, end_pos):
        text = self.master.text
        text.tag_remove("sel", "1.0", END)  # 移除旧的tag
        # 已知问题: 代码高亮显示时, 无法突出显示找到的文字
        text.tag_add("sel", start_pos, end_pos)  # 添加新的tag "sel"
        #  行数 计算滚动错误
        lines = text.get('1.0', END)[:-1].count(os.linesep) + 1
        lineno = int(start_pos.split('.')[0])
        # 滚动文本框, 使被找到的内容显示 ( 由于只判断行数, 已知有bug)
        print((lineno - text['height']) / lines)
        text.yview_moveto((lineno - text['height']) / lines)  # -****- 1.2.5版
        self.master.line_text.yview_moveto((lineno - text['height']) / lines)  # -****- 1.2.5版
        text.focus_force()

    def onquit(self):
        self.withdraw()
