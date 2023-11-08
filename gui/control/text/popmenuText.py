import os
import time
import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import windnd

from gui.control.text.rowScrolledText import RowScrolledText
from gui.control.searchDialog import SearchDialog
from gui.control.replaceDialog import ReplaceDialog


class PopMenuText(RowScrolledText):

    FILETYPES = [("所有文件", "*.*")]

    def __init__(self, master=None, cnf=None, **kw):

        super(PopMenuText, self).__init__(master=master, cnf=cnf, **kw)

        self.__class__.__name__ = 'Text'
        self._dialogs = {}
        self.filename = 'UnKnow'

        self.create_popup_menu()
        self.text.bind("<Key>", self.window_onkey)

        # 拖拽模块
        windnd.hook_dropfiles(self, func=self.Dragoon)
    
    # 拖拽触发DEF
    def Dragoon(self, files):
        # 将拖拽的文件循环便利出来并解码 存储到列表内
        for a in files:
            a = a.decode('gbk')  # 解码
            if os.path.isfile(a) == False:  # 检测是否是文件 是文件True 否则False
                pass
            else:
                self.filename =str(a).replace('\\', '/')  # 存储文件路径
                self.load(self.filename)


    def create_popup_menu(self):
        self.editmenu = ttk.Menu(self.text, tearoff=False)
        master = self.text
        self.editmenu.add_command(label="剪切  ",
                                  command=lambda: self.text_change() \
                                                  == master.event_generate("<<Cut>>"))
        self.editmenu.add_command(label="复制  ",
                                  command=lambda: master.event_generate("<<Copy>>"))
        self.editmenu.add_command(label="粘贴  ",
                                  command=lambda: self.text_change() \
                                                  == master.event_generate("<<Paste>>"))
        self.editmenu.add_separator()
        self.editmenu.add_command(label="查找", accelerator="Ctrl+F",
                                  command=lambda: self.show_dialog(SearchDialog))
        self.editmenu.add_command(label="查找下一个", accelerator="F3",
                                  command=self.findnext)
        self.editmenu.add_command(label="替换", accelerator="Ctrl+H",
                                  command=lambda: self.show_dialog(ReplaceDialog))

        self.text.bind("<Button-3>",
                       lambda event: self.editmenu.post(event.x_root, event.y_root))

        self.editmenu.add_separator()
        self.editmenu.add_command(label="New", accelerator="Ctrl+S",
                                  command=lambda: self.new())

        self.editmenu.add_command(label="Open", accelerator="Ctrl+O",
                                  command=lambda: self.open())

        self.editmenu.add_command(label="Save", accelerator="Ctrl+S",
                                  command=lambda: self.save())

        self.editmenu.add_command(label="Save As", accelerator="Ctrl+S",
                                  command=lambda: self.save_as())

    def save_as(self):
        input_file = filedialog.asksaveasfilename(filetypes=[("所有文件", "*.*"), ("文本文档", "*.text")])

        if input_file:
            self.file_name = input_file
            self.write_to_file(self.file_name)

        # 文件的保存,是保存（替代）原有文本文件的内容，先读写文件

    def write_to_file(self, file_name):
        try:
            content = self.text.get(1.0, ttk.END)
            with open(file_name, 'w', encoding='utf-8') as _file:
                _file.write(content)
            # self.title("{}---NotePad".format(os.path.basename(file_name)))
        except IOError:
            messagebox.showerror("错误", "文件保存失败！")

    def _edit_event(self, event=None):
        print(event)

    def text_change(self, event=None):
        self.file_modified = True
        # self.update_status()
        # self.change_title()

    def create(self):
        # 创建一个顶级弹窗
        top = ttk.Toplevel(title="My Toplevel", alpha=0.4, size=(1000, 1000))
        top.place_window_center()
        l = ttk.Label(top, text='2')
        l.pack()
        return top


    def show_dialog(self, dialog_type):
        # dialog_type是对话框的类型
        if dialog_type in self._dialogs:
            # 不再显示新的对话框
            d = self._dialogs[dialog_type]
            d.state(ttk.NORMAL)  # 恢复隐藏的窗口
            d.focus_force()
        else:
            d = dialog_type(self)
            d.show()
            self._dialogs[dialog_type] = d


    def findnext(self):
        fd = self._dialogs.get(SearchDialog, None)
        if fd:
            if fd.findnext():
                return
        rd = self._dialogs.get(ReplaceDialog, None)
        if rd:
            rd.findnext()

    def window_onkey(self, event):
        # 如果按下Ctrl键
        if event.state in (4, 6, 12, 14, 36, 38, 44, 46):  # 适应多种按键情况(Num,Caps,Scroll)
            key = event.keysym.lower()
            if key == 'o':  # 按下Ctrl+O键
                self.open()
                pass
            elif key == 's':  # Ctrl+S键
                self.save()
                pass
            elif key == 'n':
                self.new()
                pass
            elif key == 'f':
                self.show_dialog(SearchDialog)
            elif key == 'h':
                self.show_dialog(ReplaceDialog)
            elif key == 'equal':  # Ctrl+ "+" 增大字体
                # self.increase_font()
                pass
            elif key == 'minus':  # Ctrl+ "-" 减小字体
                # self.decrease_font()
                pass
        elif event.keysym.lower() == 'f3':
            self.findnext()
        elif event.keycode == 93:  # 按下了菜单键
            self.editmenu.post(self.winfo_x() + self.winfo_width(),
                               self.winfo_y() + self.winfo_height())

    def new(self):
        self.text.delete(1.0, ttk.END)
        self.filename = 'UnKnow'
        self.file_modified = False

    def open(self):
        # 加载一个文件
        # if self.ask_for_save(quit=False)==0:return
        filename = filedialog.askopenfilename(master=self, title='打开',
                                            initialdir=os.path.split(self.filename)[0],
                                            filetypes=self.FILETYPES
                                            )
        if not filename:
            return
        if not self.filename and not self.file_modified:  # 如果是刚新建的, 在当前窗口中打开
            self.load(filename)
        else:
            self.load(filename)

    def save(self):
        # 保存文件
        if not self.filename or self.filename == 'UnKnow':
            self.filename = filedialog.asksaveasfilename(master=self,
                                                       initialdir=os.path.split(self.filename)[0],
                                                       filetypes=self.FILETYPES)
        filename = self.filename
        if filename.strip():
            try:
                text = self.text.get('1.0', ttk.END)[:-1]  # [:-1]: 去除末尾换行符
                # data = bytes(text, encoding='utf-8', errors='replace')
                # Text文本框的bug:避免多余的\r换行符
                # 如:输入文字foobar, data中变成\rfoobar
                # data = data.replace(b'\r', b'')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.filename = filename
                self.file_modified = False
            except Exception as err:
                self.handle(err)
        else:
            return 0  # 0表示cancel

    def load(self, filename):
        # 加载文件
        try:
            t0 = time.time()
            # data = self._load_data(filename)
            try:
                self.text.delete('1.0', ttk.END)
                self.text.mark_set(ttk.INSERT, "1.0")
                for chunk in self.read_in_chunks(filename):
                    self.text.insert(ttk.INSERT, chunk)
                self.filename = filename
            except Exception as e:
                self.text.delete('1.0', ttk.END)
                self.text.insert(ttk.INSERT, e.__str__())

            self.text.mark_set(ttk.INSERT, "1.0")
            self.file_modified = False
            self.scroll_top()
            t2 = time.time()
            print(t2-t0)

            self.text.edit_reset()  # -*****- 1.2.5版: 重置文本框的撤销功能
            self.text.focus_force()
        except Exception as err:
            self.handle(err)

    # def _load_data(self, filename):
    #     # 从文件加载数据
    #     global data
    #     f = open(filename, "r", encoding="UTF-8")
    #     try:
    #         # 读取文件,并对文件内容进行编码
    #         data = f.read()
    #     except Exception as e:
    #         f.seek(0)
    #         data = e.__str__()
    #     finally:
    #         f.close()
    #         return data

    def read_in_chunks(self, file, chunk_size=1024 * 1024* 100):
        """
        Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1M
        You can set your own chunk size
        """
        f = open(file, "r", encoding="UTF-8")
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                f.close()
                break
            yield chunk_data

    def handle(err, parent=None):
        # showinfo()中,parent参数指定消息框的父窗口
        messagebox.showinfo("错误", type(err).__name__ + ': ' + str(err), parent=parent)
