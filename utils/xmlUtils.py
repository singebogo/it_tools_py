# -*-coding:utf-8-*-
'''
    XML 被设计用来传输和存储数据。可扩展标记语言（英语：Extensible Markup Language，简称：XML）是一种标记语言，
    是从标准通用标记语言（SGML）中简化修改出来的。它主要用到的有可扩展标记语言、可扩展样式语言（XSL）、XBRL和XPath等。

    XML 指可扩展标记语言（EXtensible Markup Language）。
    XML 是一种很像HTML的标记语言。
    XML 的设计宗旨是传输数据，而不是显示数据。
    XML 标签没有被预定义。您需要自行定义标签。
    XML 被设计为具有自我描述性。
    XML 是 W3C 的推荐标准。

    ElementTree 方式：ElementTree 相对于 DOM 来说拥有更好的性能，与 SAX 性能差不多，API 使用也很方便。
'''

import xml.dom.minidom as MiniDom
import xml.etree.ElementTree as ETree

try:
    import xml.sax.saxutils
    import os
except ImportError:
    raise ImportError("requires xml.sax.saxutils package, pleas check if xml.sax.saxutils is installed!")
import base64
import logging

logger = logging.getLogger(__name__)

__all__ = ["escape", "unescape"]


def xml_format(uglyxml):
    if validate_xml_string(uglyxml):
        try:
            dom_string = MiniDom.parseString(uglyxml).toprettyxml(indent="\t", newl="\n", encoding=None)
            return os.linesep.join([s for s in dom_string.splitlines() if s.strip()])
        except Exception as e:
            return e.__str__()


def validate_xml_string(xml):
    # 从xml格式字符串导入数据
    try:
        root = ETree.fromstring(xml)
        ETree.iselement(root)
        return True
    except Exception as e:
        return e.__str__()


def parsing_xml_string(xml):
    try:
        return ETree.fromstring(xml)
    except Exception as e:
        return None

def has_childs(root, tag):
    return root.iter(tag)

def validate_xml_file(xmlFile):
    try:
        tree = ETree.parse(xmlFile)
        root = tree.getroot()
        ETree.iselement(root)
        return True
    except Exception as e:
        return e.__str__()


def save_xml_string(filename, xml):
    try:
        if (validate_xml_string):
            root = ETree.fromstring(xml)
            tree = ETree.ElementTree(root)
            tree.write(filename)
    except Exception as e:
        return e.__str__()


def save_xml(filename, tree):
    try:
        tree.write(filename)
    except Exception as e:
        return e.__str__()


def load_file(filename):
    try:
        return ETree.parse(filename).getroot()  # 获取root tag
    except Exception as e:
        return e.__str__()


def valid_XML_char_ordinal(c):
    """
    @summary:
            check if the char is a valid xml character
    @param c: the character to be checked
    @see: # http://www.w3.org/TR/2008/REC-xml-20081126/#charsets
    @result: True/False
    """
    return (  # conditions ordered by presumed frequency
            0x20 <= c <= 0xD7FF
            or c in (0x09, 0x0A, 0x0D)
            or 0xE000 <= c <= 0xFFFD
            or 0x10000 <= c <= 0x10FFFF
    )


def escape(data):
    """
    @summary:
            Escape '&', '<', and '>' in a string of data.
            if the data is not ascii, then encode in base64
    @param data: the data to be processed
    @return
        {"base64": True | False,
         "data": data}
    """

    # check if all of the data is in ascii code
    is_base64 = False
    escaped_data = ""
    try:
        # data.decode("ascii")
        if data is None:
            data = ""

        is_base64 = False
        for c in data:
            if not valid_XML_char_ordinal(c):
                is_base64 = True
                break
        # check if need base64 encode
        if is_base64:
            logger.debug("%s is not ascii-encoded string, so i will encode it in base64")
            # base64 encode
            escaped_data = base64.b64encode(data)
        else:
            # check if the data should be escaped to be stored in xml
            escaped_data = xml.sax.saxutils.escape(data)

    except Exception as e:
        logger.error(e)

    return {"base64": is_base64,
            "data": escaped_data}


def unescape(data, is_base64=False):
    """
    @summary:
            Unescape '&', '<', and '>' in a string of data.
            if base64 is True, then base64 decode will be processed first
    @param data: the data to be processed
    @param base64: specify if the data is encoded by base64
    @result: unescaped data
    """
    # check if base64
    unescaped_data = data
    if is_base64:
        try:
            unescaped_data = base64.b64decode(data)
        except Exception as ex:
            logger.debug("some excpetion occured when invoke b64decode")
            logger.error(ex)
            print(ex)
    else:
        # unescape it
        unescaped_data = xml.sax.saxutils.unescape(data)

    return unescaped_data


def remove_whitespace(node):
   if node.nodeType == MiniDom.Node.TEXT_NODE:
       if node.nodeValue.strip() == "":
           node.nodeValue = ""
       for child in node.childNodes:
         remove_whitespace(child)