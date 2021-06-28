import pandas as pd
import time
from datetime import datetime
import numpy as np

# df = pd.DataFrame({'1': '2'},index=[0])
#
# df.to_excel('hello.xlsx',sheet_name='1')
# df.to_excel('hello.xlsx',sheet_name='2')
# df.to_excel('hello.xlsx',sheet_name='3')

# d = []
#
# for i in range(0,16):
#     d.append(i)
#
# print(d)

# month_card1 =  {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
#                 'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
# month_card2 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
#                'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
#
# other_packs = pd.DataFrame([month_card1, month_card2])
# print(month_card1)

# s1 = '202005050500'
# s2 = '202006050500'
#
# t1 = datetime.strptime(s1, '%Y%m%d%H%M')
# t2 = datetime.strptime(s2, '%Y%m%d%H%M')
# print(t1)
#
# qualities = []
# for i in range(4):
#     qualities.append([])
#     for j in range(3):
#         qualities[i].append(0)
#
# print(qualities)

# p = np.arange(1,5,1)

# <color, size, b, material
# <quad
# s = '<color=#111>hello <b> world </b> </color>'
# color_head = s.count('<color')
# color_end = s.count('/color')
# print(color_head, color_end)

# def check_is_error(id, lang):
#     if lang.count('<color') != lang.count('/color>'):
#         print(id, ',color 代码不匹配,', lang)
#     if lang.count('<size') != lang.count('/size>'):
#         print(id, ',size 代码不匹配,', lang)
#     if lang.count('<b') != lang.count('/b>'):
#         print(id, ',b 代码不匹配,', lang)
#     if lang.count('<material') != lang.count('/material>'):
#         print(id, ',material 代码不匹配,', lang)
#     if lang.count('<quad') != lang.count('/>'):
#         print(id, ',size 代码不匹配,', lang)
#
# path = 'languages.xlsx'
#
# language = pd.read_excel(path,sheet_name='英语',header=None)
# print('正在检测处理英语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')
#
# language = pd.read_excel(path,sheet_name='德语',header=None)
# print('正在检测处理德语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')
#
# language = pd.read_excel(path,sheet_name='法语',header=None)
# print('正在检测处理法语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')
#
# language = pd.read_excel(path,sheet_name='西语',header=None)
# print('正在检测处理西语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')
#
# language = pd.read_excel(path,sheet_name='葡语',header=None)
# print('正在检测处理葡语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')
#
# language = pd.read_excel(path,sheet_name='土语',header=None)
# print('正在检测处理土语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')
#
# language = pd.read_excel(path,sheet_name='俄语',header=None)
# print('正在检测处理俄语：')
# language.apply(lambda x:check_is_error(x[0],str(x[1])),axis=1)
# print('处理完毕')

for i in range(10,10):
    print(i)