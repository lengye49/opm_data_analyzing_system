import pandas as pd
from load_hero_info import load_hero_power

# hero_list = [1, 2, 8, 10, 11, 12, 13, 18, 19, 20, 21, 23, 24, 25, 26, 27, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42,
#              43, 44, 45, 46, 49, 51, 60, 61, 62, 63, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 100,
#              101, 102, 103]
hero_list = [100, 101, 112]

df_hero_info = pd.read_excel('design/hero_design.xlsx', sheet_name='卡牌设定', index_col=0, header=0)
collect_index = 0  # 统计的序号，hero_design表设定状态的序号，从0开始

power_base = []
power_equip = []
power_talent = []
power_academy = []
power_job = []
power_mechanical = []
power_limiter = []
power_total = []


def get_camp(_id):
    return df_hero_info.loc[_id, '_camp']


def get_limiter_on(_id):
    return df_hero_info.loc[_id, '_limiter_on']


for _id in hero_list:
    print('Doing ' + str(_id))
    _base, _equip, _talent, _academy, _job, _mechanical, _limiter, _total =\
        load_hero_power(_id, collect_index)

    power_base.append(_base)
    power_equip.append(_equip)
    power_talent.append(_talent)
    power_academy.append(_academy)
    power_job.append(_job)
    power_mechanical.append(_mechanical)
    power_limiter.append(_limiter)
    power_total.append(_total)

data = {'Id': hero_list,
        'Base': power_base,
        'Equip': power_equip,
        'Talent': power_talent,
        'Academy': power_academy,
        'Job': power_job,
        'Mechanical': power_mechanical,
        'Limiter': power_limiter,
        'Total': power_total}

df = pd.DataFrame(data, index=hero_list)
df['Base_Per'] = df['Base'] / df['Total']
df['Equip_Per'] = df['Equip'] / df['Total']
df['Talent_Per'] = df['Talent'] / df['Total']
df['Academy_Per'] = df['Academy'] / df['Total']
df['Job_Per'] = df['Job'] / df['Total']
df['Mechanical_Per'] = df['Mechanical'] / df['Total']
df['Limiter_Per'] = df['Limiter'] / df['Total']
df['Total_Per'] = df['Total'] / df['Total']

df['LimiterOn'] = df['Id'].apply(get_limiter_on)
df['Camp'] = df['Id'].apply(get_camp)

ave_all_base = int(df['Base'].mean())
ave_complete_base = int(df.loc[df['Camp'] == 5, 'Base'].mean())
ave_four_type_base = int(df.loc[df['Camp'] != 5, 'Base'].mean())
ave_total_on = int(df.loc[df['LimiterOn'] == 1, 'Total'].mean())
ave_total_on_5 = int(df.loc[(df['LimiterOn'] == 1) & (df['Camp'] == 5), 'Total'].mean())
ave_total_on_1 = int(df.loc[(df['LimiterOn'] == 1) & (df['Camp'] != 5), 'Total'].mean())
ave_total_off = int(df.loc[df['LimiterOn'] == 0, 'Total'].mean())
ave_total_off_5 = int(df.loc[(df['LimiterOn'] == 0) & (df['Camp'] == 5), 'Total'].mean())
ave_total_off_1 = int(df.loc[(df['LimiterOn'] == 0) & (df['Camp'] != 5), 'Total'].mean())
print(ave_all_base, ave_complete_base, ave_four_type_base)

# 比较全能和非全能角色的战力差

