import ttkbootstrap as ttk
from gui.control.text.popmenuText import PopMenuText

from gui.control.tree.xmlTreeview import XMLTreeview
import utils.xmlUtils as xmlUtils


class XmlPrettifyAndFormatFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.init_top_frame()
        self.init_left_frame()
        self.init_right_frame()

    def init_top_frame(self):
        top_frame = ttk.Frame(self)
        t1 = ttk.Frame(top_frame)

        self.clear_button = ttk.Button(t1, bootstyle=ttk.WARNING, text='清空')
        self.clear_button.pack(side=ttk.LEFT, expand=True)
        self.clear_button.config(command=self.clear)

        self.format_button = ttk.Button(t1, bootstyle=ttk.SUCCESS, text='格式化')
        self.format_button.pack(side=ttk.LEFT, expand=True)
        self.format_button.config(command=self.format)

        self.copy_button = ttk.Button(t1, bootstyle=ttk.SUCCESS, text='复制结果')
        self.copy_button.pack(side=ttk.LEFT, expand=True)
        self.copy_button.config(command=self.copy)


        t1.pack(fill=ttk.BOTH, expand=ttk.YES)
        top_frame.pack(fill=ttk.BOTH, expand=ttk.YES)

    def init_left_frame(self):
        left_frame = ttk.Frame(self)

        self.orgin_xml_text = PopMenuText(left_frame, bootstyle='info', padding=5, width=60, height=60, autohide=True, vbar=True)
        self.orgin_xml_text.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=ttk.YES)

        self.format_xml_text = PopMenuText(left_frame, bootstyle='info',  width=60, padding=5, autohide=True, vbar=True, hbar=True)
        self.format_xml_text.pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=ttk.YES)

        left_frame.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=True)

    def init_right_frame(self):
        right_frame = ttk.Frame(self)
        self.treeview = XMLTreeview(right_frame)
        self.treeview.pack(fill=ttk.BOTH, expand=1)
        right_frame.pack(fill=ttk.BOTH, side=ttk.LEFT, expand=ttk.YES, )

    def clear(self):
        self.format_xml_text.new()
        self.orgin_xml_text.new()
        self.treeview.delete_all()

    def format(self):
        origin_xml = self.orgin_xml_text.get(1.0, ttk.END)
        if origin_xml and len(origin_xml) > 0 and origin_xml != '\n':
            if xmlUtils.validate_xml_string(origin_xml):
                self.format_xml_text.delete(1.0, ttk.END)
                format = xmlUtils.xml_format(origin_xml)
                self.format_xml_text.insert(ttk.END, format)
                # 节点解析 并且 加载
                self.treeview.delete_all()
                if xmlUtils.validate_xml_string(format):
                    self.treeview.load_tree( format)

    def copy(self):
        try:
            import pyperclip
            pyperclip.copy(self.format_xml_text.get(1.0, ttk.END))
        except Exception as e:
            return