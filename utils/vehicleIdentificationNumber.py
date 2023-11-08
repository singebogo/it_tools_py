# -*-coding:utf-8-*-
'''
    VIN 规则算法部分
'''
import random
import string
import pandas as pd


lists = {
    "A": 1,    "B": 2,    "C": 3,    "D": 4,    "E": 5,    "F": 6,    "G": 7,    "H": 8,    "J": 1,    "K": 2,
    "L": 3,    "M": 4,    "N": 5,    "P": 7,    "R": 9,    "S": 2,    "T": 3,    "U": 4,    "V": 5,    "W": 6,
    "X": 7,    "Y": 8,    "Z": 9,
    "0": 0,    "1": 1,    "2": 2,    "3": 3,    "4": 4,    "5": 5,    "6": 6,    "7": 7,    "8": 8,    "9": 9,
}
df = pd.DataFrame(lists, index=[0])#变成dataframe类型，打印结果如下效果
#   A  B  C  D  E  F  G  H  J  K  L  M  N  ...  X  Y  Z  0  1  2  3  4  5  6  7  8  9
#0  1  2  3  4  5  6  7  8  1  2  3  4  5  ...  7  8  9  0  1  2  3  4  5  6  7  8  9


def check_vin(text):
    if len(text) == 17:#判断它是否为17位数
        text = text.upper()#小写字母转化为大写字母
        text1 = text.replace("Q","0").replace("O","0").replace("I","1")#替换文本中的字母
        if(text.find("Q") != -1 or text.find("O") != -1 or text.find("I") != -1):
            return "含有QOI-不符合规范"
        Nums = bitWeight(text1)
        # 如果余数是10 则是X
        try:
            if (''.join(text1[8]).isdigit() or ''.join(text1[8]).upper() == 'X'):
                # 如果余数是10 则是X
                return "符合规范" if Nums % 11 == (10 if (Nums % 11 == 10) else int(text1[8])) else "不符合规范"
            else:
                return '不符合规范'
        except Exception as e:
            return e.__str__()+'-不符合规范'
    else:
        return "长度不是17位数-不符合规范"


def generate_random_string(length):
    # 生成包含大小写字母和数字的序列
    characters = string.ascii_uppercase.replace('Q', '').replace('I', '').replace('O', '') + string.digits
    # 随机选择 length 个字符
    return ''.join(random.choice(characters) for i in range(length))


def getPostion(text):
    positions = []
    for i in range(17):
        if i != 8:
            positions.append(int(df[text[i]].to_string()[-1]))
        else:
            positions.append('X')
    return positions


def bitWeight(text):
    pos = getPostion(text)

    posSum = 0
    for i in range(17):
        if i < 7:
            posSum = posSum + pos[i]*(8 - i)
        elif i == 7:
            posSum = posSum + pos[i] * (i + 3)
        elif i == 8:
            # 不参与计算
            pass
        else:
            posSum = posSum + int(pos[i]) * (9 - (i - 9))
    return posSum


def get_normal_vin():
    strLeft = generate_random_string(8)
    strRight = generate_random_string(8)
    Nums = bitWeight(strLeft+'X'+strRight)
    # 如果余数是10 则是X
    str9 = 'X' if(Nums % 11 == 10) else ''.join(str(Nums % 11))
    return strLeft+str9+strRight

def get_normal_vin1(left, right):
    strLeft = left
    strRight = right
    Nums = bitWeight(strLeft+'X'+strRight)
    # 如果余数是10 则是X
    str9 = 'X' if(Nums % 11 == 10) else ''.join(str(Nums % 11))
    return strLeft+str9+strRight

def vin_numbers(number = 10):
    vins = []
    for i in range(number):
        vins.append(get_normal_vin())
    return vins