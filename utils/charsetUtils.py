
def view_hex(byte):
    result = ''
    if hasattr(bytes, 'hex'):
        conv_hex = bytes.hex
    else:  # 低于Python 3.5(如3.4版), 没有bytes.hex内置方法
        conv_hex = lambda b: hex(int.from_bytes(b, 'big'))[2:] \
            .zfill(len(b) * 2)
    for i in range(0, len(byte)):
        result += conv_hex(byte[i:i + 1]).zfill(2) + ' '
        if (i + 1) % 4 == 0: result += '\n'
    return result


def to_escape_str(byte, linesep=True):
    # 将字节(bytes)转换为转义字符串
    # linesep: 是否以length间隔加入换行符, 加入换行符可提高Text控件的显示速度
    str = ''
    length = 1024
    for i in range(0, len(byte), length):
        str += repr(byte[i: i + length])[2:-1]
        if linesep: str += '\n'
    return str


def to_bytes(escape_str):
    # 将转义字符串转换为字节
    # -*****- 1.2.5版更新: 忽略二进制模式中文字的换行符
    escape_str = escape_str.replace('\n', '')
    escape_str = escape_str.replace('"""', '\\"\\"\\"')  # 避免引号导致的SyntaxError
    escape_str = escape_str.replace("'''", "\\'\\'\\'")
    try:
        return eval('b"""' + escape_str + '"""')
    except SyntaxError:
        return eval("b'''" + escape_str + "'''")


def bell_(widget=None):
    try:
        import winsound
        winsound.PlaySound('.', winsound.SND_ASYNC)
    except (ImportError, RuntimeError):
        if widget is not None: widget.bell()


def handle(err, parent=None):
    # showinfo()中,parent参数指定消息框的父窗口
    import tkinter.messagebox as msgbox
    msgbox.showinfo("错误", type(err).__name__ + ': ' + str(err), parent=parent)