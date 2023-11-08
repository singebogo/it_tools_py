import ttkbootstrap as ttk

from utils.frameTypes import frameTypes


class ControlFrame(ttk.LabelFrame):

    def __init__(self, container):
        super(ControlFrame, self).__init__(container)
        self.container = container
        self.notebook = self.initNoteBook(container)
        self.initNoteBookChildFrame()

    def initNoteBook(self, container):
        f = ttk.Frame(container)
        f.pack(pady=5, fill=ttk.X, side=ttk.TOP)

        notebook = ttk.Notebook(f)
        notebook.pack(
            side=ttk.LEFT,
            padx=(2, 2),
            expand=ttk.YES,
            fill=ttk.BOTH,
        )
        return notebook

    def initNoteBookChildFrame(self):
        for type in frameTypes:
            self.notebook.add(type['frame'](self.container), text=type["notebook-text"])