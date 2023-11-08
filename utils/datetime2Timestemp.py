import time
'''
    unix时间戳（timestamp）是指从1970年1月1日（UTC/GMT的午夜）开始经过的秒数。在Python中，时间戳是一个浮点数，可以精确到微秒（千万分之一秒）
'''


def currentTimestamp():
    return time.time()

def currentDatetime():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def timestamp2Datetime(timestamp):
    if not timestamp:
        return None
    try:
        if not '.' in timestamp:
            if len(timestamp) > 10:
                timestamp = float(timestamp[0:11] + '.' + timestamp[11:])
        else:
            timestamp = float(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))  # 转换为字符串
    except Exception as e:
        return None


def datetime2Timestamp(datetime):

    if not datetime:
        return None
    try:
        time_tuple = time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        # 将时间元组转换为时间戳
        return time.mktime(time_tuple)
    except Exception as e:
        return None