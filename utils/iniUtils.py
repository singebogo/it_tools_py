import configparser
import os


def get_ini_path(reactive_path):
    cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(cur_path, reactive_path)


def read(file, section, option):
    conf = configparser.ConfigParser()  # 类的实例化
    conf.read(file, encoding="utf-8")
    return conf[section][option]


def set1(file, section, option, value=None):
    conf = configparser.ConfigParser()  # 类的实例化
    conf.read(file, encoding="utf-8")
    conf.set(section, option, value)  # 往配置文件写入数据
    conf.write(open(file, 'w'))  # 保存数据


def get_config_path():
    return get_ini_path('config\\my.ini')


def read_theme():
    try:
        return read(get_config_path(), 'INSTALL', 'theme')
    except Exception as e:
        raise e.__str__()

def set_theme(value):
    set1(get_config_path(), 'INSTALL', 'theme', value)
