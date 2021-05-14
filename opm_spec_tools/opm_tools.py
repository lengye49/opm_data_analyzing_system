import os
import pandas as pd


def compare_version(v1, v2):
    if len(v1.split(".")) < 3:
        return v2
    if len(v2.split(".")) < 3:
        return v1

    a, b, c = v1.split('.')
    A, B, C = v2.split('.')
    x = int(a) * 10000 + int(b) * 100 + int(c)
    y = int(A) * 10000 + int(B) * 100 + int(C)
    if x >= y:
        return v1
    else:
        return v2


def get_version_path():
    # _p = "/Users/oas/Documents/work/github/opm_specs/specs/"
    _p = os.path.abspath('..') + "/specs/"
    folders = os.listdir(_p)
    current_version = folders[0]
    for folder in folders:
        current_version = compare_version(current_version, folder)

    return _p + current_version + '/xlsx_origin/'


def read_spec_file(file_name, path):
    _df = pd.read_excel(path + file_name + '.xlsx', header=2, sheet_name=file_name)  # 以第3行为标题读取数据
    _df.dropna(axis=0, how='all')  # 删除空行
    _df = _df.drop([0])  # 删除中文标示
    return _df.reset_index()  # 重置序号后返回


def get_specific_property(_df, target_name, column_name1, value1, column_name2='', value2=None):
    if column_name2 == '':
        n = _df[_df[column_name1] == value1].index.values.astype(int)[0]
    else:
        n = _df[(_df[column_name1] == value1) & (_df[column_name2] == value2)].index.values.astype(int)[0]
    return _df.loc[n, target_name]


def split_dict_str(_str):
    _sss = _str.split(';')
    _dict = {}
    for _ss in _sss:
        _s = _ss.split(',')
        _dict[_s[0]] = _s[1]
    return _dict


def reset_dict_str_to_dict(_origin_df, _r_name):
    _df = _origin_df
    _df[_r_name] = _df[_r_name].apply(split_dict_str)
    _list_r = _df[_r_name].values.tolist()
    _df1 = pd.DataFrame(_list_r)
    _df = pd.concat([_df, _df1], axis=1)
    return _df


def re_format_reward(_reward):
    _rs = _reward.split(';')
    _list_resource = ['coin', 'diamond', 'honor', 'guild_coin', 'exp', 'hero_exp', 'hero_powder', 'lb_coin', 'vip_exp',
                      'hero_currency', 'hero_lcc', 'friend', 'high_arena']
    _list_item = ['hero', 'equip', 'avatar', 'frame']
    _r_dict = {}
    for _r in _rs:
        _s = _r.split(',')
        # 资源类
        if _s[0] in _list_resource:
            _r_dict[_s[0]] = int(_s[1])
        # 道具类
        elif _s[0] == 'prop':
            _key = _s[0] + '_' + str(_s[1])
            _r_dict[_key] = int(_s[2])
        # 特殊奖励类，暂不考虑
        elif _s[0] in _list_item:
            pass
        # reward类，暂不考虑
        else:
            pass
    return _r_dict


# 将df中的奖励字符串转为字典
def reset_rewards_to_dict(_origin_df, _r_name):
    _df = _origin_df
    _df[_r_name] = _df[_r_name].apply(re_format_reward)
    _list_r = _df[_r_name].values.tolist()
    _df1 = pd.DataFrame(_list_r)
    _df = pd.concat([_df, _df1], axis=1)
    return _df


# 进度条控制器
def process_bar(percent, start_str='', end_str='100%', total_length=15):
    bar = ''.join(["\033[31m%s\033[0m" % '==='] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


def combine_dict(ori, adda):
    for key in ori:
        if key in adda:
            ori[key] += adda[key]
    for key in adda:
        if key not in adda:
            ori[key] = adda[key]
    return ori
