# -*-coding:utf-8-*-
import ttkbootstrap as ttk
from xml.dom.minidom import parseString, Node

from gui.control.tree.nodeTreeview import NodeTreeview


class XMLTreeview(NodeTreeview):

    def __init__(self, master):
        super().__init__(master)
        self.column("#0", width=200)
        self.heading("#0", text="Tag")
        self["columns"] = ("text", "attrib")
        self.column("text", width=60)
        self.heading("text", text="Text")
        self.column("attrib", width=150)
        self.heading("attrib", text="Attrib")

    def load_tree(self, xml):
        try:
            xmldoc = parseString(xml)
        except Exception as e:
            return
        self.normalize('', xmldoc)

    def normalize(self, parent, xmldoc):
        global attrs
        for child in xmldoc.childNodes:
            attrs = []
            if child.nodeType == Node.TEXT_NODE:
                if not child.data or child.data != '\\n\\t':
                    self.set(parent, column='text', value=(child.nodeValue if child.nodeValue else ''))
            else:
                if child.nodeType == Node.ELEMENT_NODE:
                    if child.attributes and len(child.attributes) > 0:
                        attrs = [(node.nodeName, node.value) for node in child.attributes.values()]
                    item = self.insert(parent, ttk.END, text=child.tagName,
                                       values=(child.nextSibling.data if child.nextSibling else '',
                                               attrs if attrs else ''), open=True)
                    self.normalize(item, child)
