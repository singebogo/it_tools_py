import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText

class JSONPrettifyAndFormatFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container.root)

        self.text_content = '''
        The Zen of Python, by Tim Peters

        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        Flat is better than nested.
        Sparse is better than dense.
        Readability counts.
        Special cases aren't special enough to break the rules.
        Although practicality beats purity.
        Errors should never pass silently.
        Unless explicitly silenced.
        In the face of ambiguity, refuse the temptation to guess.
        There should be one-- and preferably only one --obvious way to do it.
        Although that way may not be obvious at first unless you're Dutch.
        Now is better than never.
        Although never is often better than *right* now.
        If the implementation is hard to explain, it's a bad idea.
        If the implementation is easy to explain, it may be a good idea.
        Namespaces are one honking great idea -- let's do more of those!
        '''
        self.initTopFrame()
        self.initLeftFrame()
        self.initRightFrame()

    def initTopFrame(self):
        topFrame = ttk.Frame(self)
        t1 = ttk.Frame(topFrame)
        btn = ttk.Button(t1, bootstyle=ttk.WARNING, text='1212')
        btn.pack(side=ttk.LEFT, expand=True)
        btn = ttk.Button(t1, bootstyle=ttk.SUCCESS, text='1212')
        btn.pack(side=ttk.LEFT, expand=True)
        btn = ttk.Button(t1, bootstyle=ttk.DEFAULT, text='1212')
        btn.pack(side=ttk.LEFT, expand=True)
        btn = ttk.Button(t1, bootstyle=ttk.PRIMARY, text='1212')
        btn.pack(side=ttk.LEFT, expand=True)
        btn = ttk.Button(t1, bootstyle=ttk.LIGHT, text='1212')
        btn.pack(side=ttk.LEFT, expand=True)

        t1.pack(fill=ttk.BOTH, expand=ttk.YES)
        topFrame.pack(fill=ttk.BOTH, expand=ttk.YES)


    def initLeftFrame(self):
        leftFrame = ttk.Frame(self)

        st = ScrolledText(leftFrame, padding=5,width=60, height=60, autohide=True, vbar=True)
        st.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=ttk.YES)
        st.insert(ttk.END, self.text_content)

        st1 = ScrolledText(leftFrame,width=40, padding=5, autohide=True, vbar=True)
        st1.pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=ttk.YES)
        st1.insert(ttk.END, self.text_content)

        leftFrame.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=True)

    def initRightFrame(self):
        rightFrame = ttk.Frame(self)

        tv = ttk.Treeview(
            master=self,
            columns=[0, 1],
            show=ttk.TREEHEADINGS,
            height=5
        )
        tv.column("#0", width=140)
        tv.heading(0, text='NAME')
        tv.column(0, width=60)
        tv.heading(1, text='VALUE')
        tv.column(1, width=60)

        table_data = [
            (1, 'one'),
            (2, 'two'),
            (3, 'three'),
            (4, 'four'),
            (5, 'five'),
            (4, 'four'),
            (5, 'five')
        ]
        tv_root = tv.insert('', ttk.END, values='2', open=True)
        item = tv_root
        for row in table_data:
            item = tv.insert(item, ttk.END, values=row, open=True)

        tv.selection_set(tv_root)

        tv.pack(fill=ttk.BOTH, expand=1)

        rightFrame.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=ttk.YES, )