# -*-coding:utf-8-*
import ttkbootstrap as ttk


import utils.iniUtils as iniUtils
from gui.controlFrame.controlFrame import ControlFrame
from gui.win32.hotkey import hide
from gui.threading.stopped_able_threading import StoppableThread

title = 'it-toos'


class App(ttk.Window):

    def __init__(self, title=title,
                 themename="litera",
                 iconphoto='',
                 size=None,
                 position=None,
                 minsize=None,
                 maxsize=None,
                 resizable=None,
                 hdpi=True,
                 scaling=None,
                 transient=None,
                 overrideredirect=False,
                 alpha=1.0, ):

        super(App, self).__init__(
            title=title,
            themename=themename,
            iconphoto=iconphoto,
            size=size,
            position=position,
            minsize=minsize,
            maxsize=maxsize,
            resizable=resizable,
            hdpi=hdpi,
            scaling=scaling,
            transient=transient,
            overrideredirect=overrideredirect,
            alpha=alpha,
        )
        # noinspection PyBroadException
        try:
            themename = iniUtils.read_theme()
        except Exception as e:
            pass
        finally:
            style = ttk.Style()
            style.theme_use(themename)


        self.set_window_style()
        ttk.Separator(self).pack(fill=ttk.X, pady=10, padx=10)
        self.set_window_size()
        self.place_window_center()
        self.fullscreen = False

        self.bind("<Unmap>", self.OnUnmap)
        self.bind("<Map>", self.OnMap)
        self.bind('<F11>', self.F11)



        # hotkey win+F10
        self.hotkey = StoppableThread(target=hide, kwargs={"title": self.title, "flag": True})
        self.hotkey.setDaemon(True)  # 设置守护线程，当线程结束，守护线程同时关闭，要不然这个线程会一直运行下去。
        self.hotkey.start()



    def F11(self, even):
        self.attributes("-fullscreen", not self.fullscreen)
        self.fullscreen = not self.fullscreen

    def set_window_style(self):
        style = ttk.Style()
        theme_names = style.theme_names()  # 以列表的形式返回多个主题名
        theme_selection = ttk.Frame(self)
        theme_selection.pack(side=ttk.TOP, fill=ttk.X, expand=ttk.YES)
        lbl = ttk.Label(theme_selection, text="选择主题:")
        theme_cbo = ttk.Combobox(
            master=theme_selection,
            text=style.theme.name,
            values=theme_names,
        )
        theme_cbo.pack(padx=10, side=ttk.RIGHT)
        theme_cbo.current(theme_names.index(style.theme.name))
        lbl.pack(side=ttk.RIGHT)

        def change_theme(e):
            theme_cbo_value = theme_cbo.get()
            style.theme_use(theme_cbo_value)
            theme_selected.configure(text=theme_cbo_value)
            theme_cbo.selection_clear()
            iniUtils.set_theme(theme_cbo_value)

        theme_cbo.bind('<<ComboboxSelected>>', change_theme)

        theme_selected = ttk.Label(
            master=theme_selection,
            text=theme_cbo.get(),
            font="-size 24 -weight bold"
        )

        theme_selected.pack(side=ttk.LEFT)

    def set_window_size(self):
        sw = self.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.winfo_screenheight()
        # 得到屏幕高度
        x = 10
        y = 10
        self.geometry("%dx%d+%d+%d" % (sw * 0.8, sh * 0.8, x, y))

    def destroy(self):
        super(App, self).destroy()

        if self.hotkey.is_alive():
            self.hotkey.stop()

    def OnUnmap(self, event):
        """
         最小化
        :param event:
        :return:
        """
        # print('...OnUnmap.', event)
        pass

    def OnMap(self, event):
        """
        恢复最小化
        :param event:
        :return:
        """
        # print('..OnMap..', event)
        pass


if __name__ == '__main__':
    app = App(
        title=title,  # 设置窗口的标题
        size=(1346, 850),  # 窗口的大小
        position=(100, 100),  # 窗口所在的位置
        minsize=(1346, 850),  # 窗口的最小宽高
        maxsize=(1920, 1080),  # 窗口的最大宽高
        resizable=None,  # 设置窗口是否可以更改大小
    )
    ControlFrame(app)
    app.mainloop()
