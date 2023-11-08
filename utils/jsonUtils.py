# -*-coding:utf-8-*-
'''
    json.dumps()用于将字典形式的数据转化为字符串
    json.loads()用于将字符串形式的数据转化为字典
'''
import json
import codecs


def str2json(text):
    try:
        text = unescape_char('/"', text)
        text = unescape_char('\\"', text)
        return json.loads(text)
    except Exception as e:
        return e.__str__()


def is_json(text):
    try:
        text = unescape_char('/"', text)
        text = unescape_char('\\"', text)
        json.loads(text)
        return True
    except Exception as e:
        return e.__str__()


def is_json_bom(text):
    try:
        text = unescape_char('/"', text)
        text = unescape_char('\\"', text)
        json.loads(codecs.BOM_UTF8 + text.encode('utf-8').lstrip(codecs.BOM_UTF8))
        return True
    except Exception as e:
        return e.__str__()


def escape(text, indent=4):
    """
        转义
    """
    try:
        if not isinstance(text, dict):
            if not have_escape('/"', text) and not have_escape('\\"', text):
                text = json.loads(text)
                # 替换
                return json.dumps(text, sort_keys=True, indent=indent, separators=(',', ':'),
                                  ensure_ascii=False).replace('"', '/"')
            else:
                return text
    except Exception as e:
        return e.__str__()


def unescape_char(str, text):
    if ''.join(text).find(str) != -1:
        return json.loads(''.join(text).replace(str, '"'))
    else:
        return text


def have_escape(str, text):
    if ''.join(text).find(str) != -1:
        return True
    else:
        return False


def unescape(text, indent=4):
    """
    去转义
    :param text:
    :param indent: 制表符
    :return:
    """
    try:
        if not isinstance(text, dict):
            # Return -1 on failure.
            if not have_escape('/"', text) and not have_escape('\\"', text):
                return text
            else:
                text = unescape_char('/"', text)
                text = unescape_char('\\"', text)
        # 替换
        return json.dumps(text, sort_keys=True, indent=indent, separators=(',', ':'), ensure_ascii=False)
    except Exception as e:
        return e.__str__()


def format(text, indent=4):
    try:
        if not isinstance(text, dict):
            if not have_escape('/"', text) and not have_escape('\\"', text):
                text = json.loads(text)
            else:
                text = unescape_char('/"', text)
                text = unescape_char('\\"', text)
        return json.dumps(text, sort_keys=True, indent=indent, separators=(',', ':'), ensure_ascii=False)
    except Exception as e:
        return e.__str__()


def compress(text):
    try:
        if not isinstance(text, dict):
            # Return -1 on failure.
            if ''.join(text).find('/"') != -1:
                text = json.loads(''.join(text).replace('/"', '"'))
                return json.dumps(text, ensure_ascii=False).replace('"', '/"')
            elif ''.join(text).find('\\"') != -1:
                text = json.loads(''.join(text).replace('\\"', '"'))
                return json.dumps(text, ensure_ascii=False).replace('"', '\\"')
            else:
                text = json.loads(text)
                return json.dumps(text, ensure_ascii=False)
    except Exception as e:
        return e.__str__()
