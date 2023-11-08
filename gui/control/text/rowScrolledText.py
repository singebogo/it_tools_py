# -*-coding:utf-8-*-
import tkinter as tk
from ttkbootstrap.constants import *

from gui.control.text.scrolledText import ScrolledText


class RowScrolledText(ScrolledText):

    def __init__(self, master=None,
                 padding=2,
                 bootstyle=DEFAULT,
                 autohide=False,
                 vbar=True,
                 hbar=False,
                 nbar=True,
                 **kwargs, ):
        super(RowScrolledText, self).__init__(master=master,
                                              padding=padding,
                                              bootstyle=bootstyle,
                                              autohide=autohide,
                                              vbar=vbar,
                                              hbar=hbar,
                                              **kwargs, )

        spacing = 0
        # font = ("等线等线 (Light)", 12)
        #  需要同时设置 text line_text 字体 font=font,spacing3=spacing,

        if nbar:
            self.line_text = tk.Text(self, width=1, bg="#808080", state="disabled", cursor="arrow")

            self.line_text.pack(side=LEFT, expand='no', fill=Y)
        self.text.pack(side=RIGHT, fill="both", expand=True)

        if vbar:
            self.vbar.configure(command=self.scroll)
        events = self.text.event_info()

        # 每行插入数字,用来对比行数显示的效果
        # for i in range(60):
        #     self.text.insert('end', str(i + 1) + "\n")
        if nbar:
            self.line_text.bind("<MouseWheel>", self.wheel)  # line_text鼠标滚轮事件
            self.text.bind("<MouseWheel>", self.wheel)  # ScrolledText鼠标滚轮事件

            # linux
            # self.text.bind("<Button-1>", self.wheel)  #  <Button-1>表示鼠标左键，
            # self.text.bind("<Button-2>", self.wheel)  #  <Button-2>表示鼠标中键，
            # self.text.bind("<Button-3>", self.wheel)  #  <Button-3>表示鼠标右键，
            # self.text.bind("<Button-4>", self.wheel)  # 表示滚轮上滑（Linux）
            # self.text.bind("<Button-5>", self.wheel)  # 表示滚轮下滑（Linux）
            # self.line_text.bind("<Button-5>", self.wheel)  # line_text鼠标滚轮事件
            # self.line_text.bind("<Button-4>", self.wheel)  # line_text鼠标滚轮事件

            self.text.bind("<KeyPress-Up>", self.KeyPress_scroll)
            self.text.bind("<KeyPress-Down>", self.KeyPress_scroll)
            self.text.bind("<KeyPress-Left>", self.KeyPress_scroll)
            self.text.bind("<KeyPress-Right>", self.KeyPress_scroll)
            self.text.bind("<<Selection>>", self.on_selection)  # 文本选中事件
            self.text.bind("<<TextModified>>", self.get_txt)  # 绑定文本修改事件

            self.text.bind('<Motion>', self.mouseMove)  # 鼠标移动
            self.show_line()  # 显示行数

    def mouseMove(self, event):
        # print('当前位置：', event.x, event.y)
        pass

    def on_selection(self, event):  # 处理选中文本事件
        # text = event.widget.get("sel.first", "sel.last")  # 获取选中文本的内容
        self.line_text.yview('moveto', self.vbar.get()[0])  # 确保选中拖动导致滚动条滚动时行数显示能同步

    def scroll(self, *xy):  # 处理滚动条滚动事件
        # 根据滚动条,更新line_text和ScrolledText的垂直滚动位置
        self.line_text.yview(*xy)
        self.text.yview(*xy)

    def scroll_top(self):  # 处理滚动条滚动事件
        # 根据滚动条,更新line_text和ScrolledText的垂直滚动位置
        self.line_text.yview(*('moveto', 0.0))
        self.text.yview(*('moveto', 0.0))

    def get_txt(self, event=None):  # 用于获取文本内容并显示
        """修改内容后需要的操作都可以写在这里"""
        txt = self.text.get("1.0", "end")[:-1]  # 文本框内容
        self.show_line()

    def show_line(self):
        # 获取文本行数
        text_lines = int(self.text.index('end-1c').split('.')[0])
        # 计算行数最多右几位数,调整
        len_lines = len(str(text_lines))
        self.line_text['width'] = len_lines + 2

        # 将显示行数文本的状态设置为正常
        self.line_text.configure(state="normal")
        # 删除行文本中的所有内容
        self.line_text.delete("1.0", "end")

        # 遍历文本数组,逐行插入到行文本中
        for i in range(1, text_lines + 1):
            if i == 1:
                self.line_text.insert("end", " " * (len_lines - len(str(i)) + 1) + str(i))
            else:
                self.line_text.insert("end", "\n" + " " * (len_lines - len(str(i)) + 1) + str(i))

        self.scroll('moveto', self.vbar.get()[0])  # 模拟滚动条滚动事件

        self.line_text.configure(state="disabled")  # 将行文本的状态设置为禁用

        self.KeyPress_scroll(row=1)  # 处理光标超过显示范围事件,否则行数会不同步

    def KeyPress_scroll(self, event=None, moving=0, row=0):
        # 光标所在行的行数和位置
        line, column = map(int, self.text.index("insert").split('.'))
        # 屏幕显示范围最上面的行
        first_line = int(self.text.index("@0,0").split('.')[0])
        # 屏幕显示范围最下面的行
        last_line = int(self.text.index("@0," + str(self.text.winfo_height())).split('.')[0])

        # 光标超显示范围事件,先滚动屏幕到光标能显示区域
        if line <= first_line + row or line >= last_line - row:
            self.see_line(line)

        if row:
            return  # show_line 转过来的到这里结束

        if event.keysym == 'Up':  # 按上键,在光标小于顶部能显示的下一行时激活滚动
            if line <= first_line + 1:
                moving = -1  # 这里用first_line+1,是为了防止最上面一行只露出一点的情况,下面同理
        elif event.keysym == 'Down':  # 按下键,在光标大于底部能显示的上一行时激活滚动
            if line >= last_line - 1:
                moving = 1
        elif event.keysym == 'Left':  # 按左键,在光标小于顶部能显示的下一行且光标在开头时激活滚动
            if line <= first_line + 1 and not column:
                moving = -1
        elif event.keysym == 'Right':  # 按右键,在光标大于底部能显示的上一行且光标在结尾时激活滚动
            text = self.text.get("1.0", "end")  # 获取文本内容
            cursor_line = text.split("\n")[line - 1]  # 获取光标所在行内容
            line_length = len(cursor_line)  # 光标在当前行的位置
            if line >= last_line - 1 and column == line_length:
                moving = 1

        self.line_text.yview_scroll(moving, "units")
        self.text.yview_scroll(moving, "units")

    def see_line(self, line):
        self.text.see(f"{line}.0")
        self.line_text.see(f"{line}.0")

    def wheel(self, event):  # 处理鼠标滚轮事件
        # 根据鼠标滚轮滚动的距离,更新line_text和ScrolledText的垂直滚动位置
        self.line_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
