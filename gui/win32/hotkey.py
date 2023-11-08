import win32gui, win32con
import time


def hide(title, flag=True):
    # 第一个参数填0，意味着为当前线程添加热键，第二个99，你也可以用别的数字，自己测试下
    # 我注册的热键是win+F10
    win32gui.RegisterHotKey(0, 99, win32con.MOD_WIN, win32con.VK_F10)
    while 1:
        time.sleep(1)  # 避免频繁获取暂停一秒
        msg = win32gui.GetMessage(0, 0, 0)  # 获得本线程产生的消息，返回值是个列表
        # msg-----[1, (0, 786, 99, 7929864, 24627051, (534, 440))]
        if msg[1][2] == 99:  # 根据下标和热键id确定按下的是我们注册的热键99
            toggle_window(title, flag)
            flag = not flag  # 更改标志


def toggle_window(title, flag):
    hd = win32gui.FindWindow(0, title)  # 根据标题找到窗口句柄
    win32gui.ShowWindow(hd, flag)  # 把句柄传给showwindow实现显示隐藏效果