import tkinter as tk
import ttkbootstrap as ttk
import threading
import time

from ..control.calendar import Calendar
import utils.datetime2Timestemp as datetime2Timestemp


class TimestampFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.container = container
        # field options
        options = {'padx': 2, 'pady': 0}
        # 初始化界面
        self.initGuiCurrent(options)
        self.initGuiTimetamp2DateTime(options)
        self.initGuiDatetime2Timetamp(options)

        # add padding to the frame and show it
        self.intvalTimestamp()

    def initGuiCurrent(self, options):
        group = ttk.LabelFrame(self.container, text="当前时间&时间戳")
        group.grid(column=0, row=0, sticky='w', padx=2, pady=2)
        # temperature label
        self.timestamp_now_label = ttk.Label(group, text='当前时间戳:')
        self.timestamp_now_label.grid(column=0, row=0, sticky='w', **options)

        # timestamp_now entry
        self.timestamp_now = tk.StringVar()
        self.timestamp_now_entry = ttk.Entry(group, bootstyle=ttk.PRIMARY, textvariable=self.timestamp_now)
        self.timestamp_now_entry.grid(column=1, row=0, sticky='w', **options)
        self.timestamp_now_entry.config(state='readonly')

        # datetime label
        self.timestamp_now_datetime_label = ttk.Label(group, text='当前日期:')
        self.timestamp_now_datetime_label.grid(column=2, row=0, sticky='w', **options)

        # timestamp_now entry
        self.timestamp_now_datetime = tk.StringVar()
        self.timestamp_now_datetime_entry = ttk.Entry(group, bootstyle=ttk.PRIMARY, textvariable=self.timestamp_now_datetime)
        self.timestamp_now_datetime_entry.grid(column=3, row=0, sticky='w', **options)
        self.timestamp_now_datetime_entry.config(state='readonly')

    def initGuiTimetamp2DateTime(self, options):
        #  时间戳转换成时间日期格式
        group = ttk.LabelFrame(self.container, text="时间戳转换成时间日期格式")
        group.grid(column=0, row=1, sticky='w', padx=2, pady=2)
        self.timestamp_time_need_label = ttk.Label(group, text='时间戳:')
        self.timestamp_time_need_label.grid(column=0, row=1, sticky='w', **options)
        # timestamp_time entry
        self.timestamp_time_need = tk.StringVar()
        self.timestamp_time_need_entry = ttk.Entry(group, bootstyle=ttk.PRIMARY, textvariable=self.timestamp_time_need)
        self.timestamp_time_need_entry.grid(column=1, row=1, sticky='w', **options)

        self.convert_date_button = ttk.Button(group, text='转换成时间日期:')
        self.convert_date_button.grid(column=2, row=1, sticky='w', **options)
        self.convert_date_button.configure(command=self.timestampConvertDatetime)

        #  时间戳转换成时间日期格式
        self.timestamp_datatime_label = ttk.Label(group, text='日期:')
        self.timestamp_datatime_label.grid(column=3, row=1, sticky='w', **options)
        # temperature entry
        self.timestamp_datatime = tk.StringVar()
        self.timestamp_datatime_entry = ttk.Entry(group, bootstyle=ttk.PRIMARY, textvariable=self.timestamp_datatime)
        self.timestamp_datatime_entry.grid(column=4, row=1, sticky='w', **options)
        self.timestamp_datatime_entry.config(state='readonly')

    def initGuiDatetime2Timetamp(self, options):
        group = ttk.LabelFrame(self.container, text="时间日期格式转换时间戳")
        group.grid(column=0, row=2, sticky='w', padx=2, pady=2)
        #  时间日期转换时间戳
        self.timestamp_year_label = ttk.Label(group, text='日期:')
        self.timestamp_year_label.grid(column=0, row=2, sticky='w', **options)
        # 时间
        self.timestamp_datetime_need = tk.StringVar()
        self.timestamp_datetime_need_entry = ttk.Entry(group,  bootstyle=ttk.PRIMARY, textvariable=self.timestamp_datetime_need)
        self.timestamp_datetime_need_entry.grid(column=1, row=2, sticky='w', **options)
        self.convert_datepick_button = ttk.Button(group, width=5, text='日期', command=self.pickDateTime)
        self.convert_datepick_button.grid(column=2, row=2, sticky='w', **options)

        self.convert_timestamp_button = ttk.Button(group, text='转换成时间戳')
        self.convert_timestamp_button.grid(column=3, row=2, sticky='w', **options)
        self.convert_timestamp_button.configure(command=self.DatetimeConvertTimestamp)

        # temperature entry
        self.timestamp_time = tk.StringVar()
        self.timestamp_time_entry = ttk.Entry(group,  bootstyle=ttk.PRIMARY, textvariable=self.timestamp_time)
        self.timestamp_time_entry.grid(column=4, row=2, sticky='w', **options)
        self.timestamp_time_entry.config(state='readonly')

    def pickDateTime(self):
        datetime = Calendar([
            self.timestamp_datetime_need_entry.winfo_rootx(),
            self.timestamp_datetime_need_entry.winfo_rooty()
        ]).selection()
        self.timestamp_datetime_need.set(datetime if datetime else '')

    def timestampConvertDatetime(self):
        """  Handle button click event
        """
        if not self.timestamp_time_need:
            return
        datetime = datetime2Timestemp.timestamp2Datetime(self.timestamp_time_need.get())
        self.timestamp_datatime.set(datetime if datetime else '')

    def DatetimeConvertTimestamp(self):
        """  Handle button click event
        """
        if not self.timestamp_datetime_need:
            return
        timestemp = datetime2Timestemp.datetime2Timestamp(''.join(self.timestamp_datetime_need.get()))

        self.timestamp_time.set(timestemp if timestemp else '')

    def reset(self):
        self.timestamp_time_entry.delete(0, "end")
        self.timestamp_datatime_entry.delete(0, 'end')
        self.timestamp_time_need_entry.delete(0, 'end')
        self.timestamp_datetime_need_entry.delete(0, 'end')


    def destroy(self):
        self.timestampId.cancel() if self.timestampId else self.timestampId

    def intvalTimestamp(self):
        self.timestamp_now.set(datetime2Timestemp.currentTimestamp())
        self.timestamp_now_datetime.set(datetime2Timestemp.currentDatetime())
        self.timestampId = threading.Timer(1, self.intvalTimestamp, args=None, kwargs=None)
        self.timestampId.start()

