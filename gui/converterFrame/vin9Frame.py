import ttkbootstrap as ttk

from utils.vehicleIdentificationNumber import vin_numbers, get_normal_vin, check_vin


class Vin9Frame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.container = container
        # field options
        self.count = 10
        options = {'padx': 2, 'pady': 0}
        self.initFrame()
        self.textEntry.set(10)

        # 布局

    def initFrame(self):
        labFrame = ttk.LabelFrame(self.container, text="Vin Data Validation")  # 创建框架标签
        #
        self.initCheck(labFrame)
        self.initGenerVin(labFrame)

        labFrame.pack(padx=2, pady=10, ipadx=2, ipady=2)
        self.initText(labFrame)

    def initCheck(self, labFrame):
        self.vintextL = ttk.StringVar()
        self.vintextL.set("vin:")
        self.vinL = ttk.Label(labFrame, text="vin:", textvariable=self.vintextL)
        self.vinL.grid(row=0, column=0)

        self.vintext = ttk.StringVar()
        self.vin = ttk.Entry(labFrame, width=17, textvariable=self.vintext)
        self.vin.grid(row=0, column=1)
        self.vin.bind('<Key>', lambda e: self.TextChange(e, self.vintext))  # 给输入框绑定键盘敲击事件，把绑定的变量传入回调函数中
        # 设置文本框只能输入数字
        self.vin.config(validate="key",
                        validatecommand=(self.container.register(lambda P: P.isascii()), "%P"))

        btn = ttk.Button(labFrame, text="Check", command=self.checkCallBack)
        btn.grid(row=0, column=2)
        self.isRulesVin = ttk.Entry(labFrame, style=ttk.PRIMARY, width=10, state='readonly')
        self.isRulesVin.grid(row=0, column=3)

    def initGenerVin(self, labFrame):
        numberL = ttk.Label(labFrame, text="vin nums:")
        numberL.grid(row=1, column=0)

        self.textEntry = ttk.StringVar()

        self.number = ttk.Entry(labFrame, textvariable=self.textEntry, width=15)
        self.number.grid(row=1, column=1)
        # 设置文本框只能输入数字
        self.number.config(validate="key",
                           validatecommand=(self.container.register(lambda P: P.isdigit()), "%P"))

        generBtn = ttk.Button(labFrame, text="Gener", command=self.generBtnCallBack)
        generBtn.grid(row=1, column=2)

        generBtn = ttk.Button(labFrame, text="G-One", command=self.generOneBtnCallBack)
        generBtn.grid(row=1, column=3)

    def initText(self, labFrame):
        scrollbar_v = ttk.Scrollbar(self.container)
        scrollbar_v.pack(side=ttk.RIGHT, fill=ttk.Y)
        scrollbar_h = ttk.Scrollbar(self.container, orient=ttk.HORIZONTAL)
        scrollbar_h.pack(side=ttk.BOTTOM, fill=ttk.X)
        self.text1 = ttk.Text(self.container, yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set,
                              wrap=ttk.NONE)
        self.text1.pack(expand=ttk.YES, fill=ttk.BOTH)
        scrollbar_v.config(command=self.text1.yview)  # 垂直滚动条绑定text
        scrollbar_h.config(command=self.text1.xview)  # 水平滚动条绑定text

    def checkCallBack(self):
        if (self.vin.get()):
            self.vintextL.set('vin: ' + str(len(self.vin.get())))
            self.isRulesVin.config(state='normal')
            self.isRulesVin.delete(0, ttk.END)
            msg = check_vin(self.vin.get())
            self.isRulesVin.insert(ttk.END, msg if msg.find('-') == -1 else msg[msg.find('-') + 1:])
            self.isRulesVin.config(state='readonly')
            self.text1.insert(ttk.END, msg + "\n")

    def generBtnCallBack(self):
        if (self.number.get()):
            self.text1.delete(1.0, ttk.END)
            vins = vin_numbers(int(self.number.get()))
            for vin in vins:
                self.text1.insert(ttk.END, vin + "\n")

    def generOneBtnCallBack(self):
        self.text1.delete(1.0, ttk.END)
        self.text1.insert(ttk.END, get_normal_vin())  # END实际就是字符串'end'

    def TextChange(self, event, widgetVar):
        self.vintextL.set('vin: ' + str(len(self.vin.get())))
