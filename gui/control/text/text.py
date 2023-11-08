import tkinter as tk
from tkinter import Text, Pack, Grid, Place
import tkinter.font as tkfont

__all__ = ['ModifiedText']


class ModifiedText(tk.Text):

    def __init__(self, *args, **kwargs):
        """自定义多行文本框类，可实时监控变化事件"""

        Text.__init__(self, *args, **kwargs)

        self.__class__.__name__ = 'Text'

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self, m))

        # 为底层控件创建一个代理
        # 为变量s添加一个属性_orig,其值为s的_w属性值加上"_orig"字符串
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

        self.focus_force()

        # 设置制表符宽度
        font = tkfont.Font(font=self['font'])
        tab_size = font.measure('   ')
        self.config(tabs=tab_size)

    def _proxy(self, command, *args):
        if command == 'get' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return
        if command == 'delete' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return
        cmd = (self._orig, command) + args
        try:
            result = self.tk.call(cmd)
        except tk.TclError:
            return
        if command in ('insert', 'delete', 'replace'):
            self.event_generate('<<TextModified>>')
        return result
