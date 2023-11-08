# option-text  index  Frame
from gui.converterFrame.functionFrame import FunctionFrame
from gui.converterFrame.nodepadFrame import NotepadFrame
from gui.converterFrame.jsonPrettifyAndFormatFrame import JSONPrettifyAndFormatFrame
from gui.converterFrame.xmlPrettifyAndFormatFrame import XmlPrettifyAndFormatFrame


frameTypes = [
    {"notebook-text": "记事本", 'frame': NotepadFrame},
    {"notebook-text": "小功能", 'frame': FunctionFrame},
    {"notebook-text": "JSON prettify and format",  'frame': JSONPrettifyAndFormatFrame},
    {"notebook-text": "XML prettify and format",  'frame': XmlPrettifyAndFormatFrame},
]