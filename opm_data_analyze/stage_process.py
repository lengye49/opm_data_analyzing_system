import openpyxl
import pandas as pd
import datetime

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

df = pd.read_csv('3_cost.csv',index_col=0)
start_time = datetime.datetime.strptime('2021/3/1','%Y/%m/%d')
target_columns = 32
target_rows = int(df.shape[0] * 0.3)
print(target_rows)

column_names = list(df)
# print(column_names)
# datetime.datetime.strftime(column_names[5],'%Y-%m-%d')
# print((datetime.datetime.strptime(column_names[5],'%Y/%m/%d') - datetime.datetime.strptime(column_names[4],'%Y/%m/%d')).days)


df[column_names[0]] = df[column_names[0]].apply(lambda x:(datetime.datetime.strptime(x,'%Y-%m-%d') - start_time).days)
# print(df[column_names[0]] )
# print(df.columnns.values)

# for i in range(0,100):
#     df[i] = df.apply(df[column_names[i+3+df[column_names[0]]]])

count = 0
for index,row in df.iterrows():
    # print(index)
    for i in range(0,target_columns):
        # print(row[column_names[i+3]])
        # print(column_names[i + 3 + row[column_names[0]]])
        if i == 0:
            row[column_names[i+3]] = row[column_names[i + 3 + row[column_names[0]]]]
        else:
            row[column_names[i + 3]] = row[column_names[i + 3 + row[column_names[0]]]] + row[column_names[i+2]]
    try:
        df.loc[index] = row
    except:
        count +=1

x = []

for i in range(0, target_columns):
    x.append(df[column_names[i+3]].nlargest(target_rows, keep='all').min())
print('发生错误的数量为 %d' % count)

print(x)