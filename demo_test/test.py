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

p = np.arange(1,5,1)
