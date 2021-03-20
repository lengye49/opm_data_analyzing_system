import pandas as pd


def get_max(v1,v2,v3,v4,v5,v6,v7,v8,v9):
    _m = 0
    if v1 != '未知':
        v1 = int(v1)
        _m = _m if _m >= v1 else v1
    if v2 != '未知':
        v2 = int(v2)
        _m = _m if _m >= v2 else v2
    if v3 != '未知':
        v3 = int(v3)
        _m = _m if _m >= v3 else v3
    if v4 != '未知':
        v4 = int(v4)
        _m = _m if _m >= v4 else v4
    if v5 != '未知':
        v5 = int(v5)
        _m = _m if _m >= v5 else v5
    if v6 != '未知':
        v6 = int(v6)
        _m = _m if _m >= v6 else v6
    if v7 != '未知':
        v7 = int(v7)
        _m = _m if _m >= v7 else v7
    if v8 != '未知':
        v8 = int(v8)
        _m = _m if _m >= v8 else v8
    if v9 != '未知':
        v9 = int(v9)
        _m = _m if _m >= v9 else v9

    return _m


df = pd.read_csv('1.csv', index_col=1, header=0)
df = df.drop(df[df['s_stage.触发用户数']==0].index)
# df = pd.read_excel('1.xlsx', index_col=1, header=0)
df['lv'] = df.apply(lambda col:get_max(col['1号位突破限制器等级'],col['2号位突破限制器等级'],col['3号位突破限制器等级'],
                                       col['4号位突破限制器等级'],col['5号位突破限制器等级'],col['6号位突破限制器等级'],
                                       col['7号位突破限制器等级'],col['8号位突破限制器等级'],col['9号位突破限制器等级']),axis=1)
df = df.groupby('账户ID').agg({'lv':'max'})
df = df.groupby('lv').agg({'lv': 'count'})
df.to_excel('test.xlsx')



