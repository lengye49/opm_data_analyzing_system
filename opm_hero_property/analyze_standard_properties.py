"""
这个脚本用于对比各个功能在标准状态下的战力占比
"""

import pandas as pd
import os
from openpyxl import load_workbook


# ******************************* 设定Spec版本号 ******************************

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


def set_version_path():
    # _p = "/Users/oas/Documents/work/github/opm_specs/specs/"
    _p = os.path.abspath('..') + "/specs/"
    folders = os.listdir(_p)
    current_version = folders[0]
    for folder in folders:
        current_version = compare_version(current_version, folder)

    global path
    path = _p + current_version + '/xlsx_origin/'


# ******************************* 读取Spec:Excel文件 ******************************

def read_spec_file(file_name):
    _df = pd.read_excel(path + file_name + '.xlsx', header=2, sheet_name=file_name)  # 以第3行为标题读取数据
    _df.dropna(axis=0, how='all')  # 删除空行
    _df = _df.drop([0])  # 删除中文标示
    return _df.reset_index()  # 重置序号后返回


def get_specific_property(_df, target_name, column_name1, value1, column_name2='', value2=None):
    # 获取指定行列的值
    if column_name2 == '':
        n = _df[_df[column_name1] == value1].index.values.astype(int)[0]
    else:
        n = _df[(_df[column_name1] == value1) & (_df[column_name2] == value2)].index.values.astype(int)[0]
    return _df.loc[n, target_name]


def get_dict_from_str(_str, adder=''):
    # 将属性字符串转换为字典
    _str = str(_str)
    if _str == 'nan' or _str == '':
        return pd.Series({'AttributeInfo': None})
    _str = _str.replace(',', ':')
    _str = _str.replace(';', ',')
    _str = '{' + _str + '}'
    _dict = eval(_str)
    return pd.Series({'AttributeInfo': _dict})


def get_aura_dict_from_str(_str):
    # 读取全体光环
    return get_dict_from_str(_str,'AuraAttribute')


def get_type_aura_dict_from_str(_str):
    # 读取阵营光环
    return get_dict_from_str(_str,'TypeAuraAttribute')


def read_data_from_specs():

    print('正在读取spec数据...')

    # 1. 读取英雄基础信息
    global df_hero
    df_hero = read_spec_file('Hero')
    df_hero = df_hero.loc[:, df_hero.columns.intersection(
        ['Id', 'Rarity', 'Type', 'Role', 'HpBase', 'AtkBase', 'DefBase', 'CritBase', 'Job'])]
    df_hero = df_hero.drop(df_hero[df_hero['Id'] > 1000].index)

    # 2. 读取等级成长信息
    global df_hero_lv_growth
    df_hero_lv_growth = read_spec_file('HeroLevelGrowth')

    # 3. 读取等级突破成长信息
    global df_hero_grade_growth
    df_hero_grade_growth = read_spec_file('HeroGradeProperty')

    # 4. 读取品质成长信息
    global df_hero_quality_growth
    df_hero_quality_growth = read_spec_file('HeroQualityProperty')
    if a_type=='pve':
        df_hero_quality_growth = df_hero_quality_growth.join(
            df_hero_quality_growth['LimiterPropertyMax'].apply(get_dict_from_str))
        df_hero_quality_growth = df_hero_quality_growth.join(
            df_hero_quality_growth['LimiterAuraMax'].apply(get_aura_dict_from_str))
        df_hero_quality_growth = df_hero_quality_growth.join(
            df_hero_quality_growth['LimiterTypeAuraMax'].apply(get_type_aura_dict_from_str))
    else:
        df_hero_quality_growth = df_hero_quality_growth.join(
            df_hero_quality_growth['PvpLimiterPropertyMax'].apply(get_dict_from_str))
        df_hero_quality_growth = df_hero_quality_growth.join(
            df_hero_quality_growth['PvpLimiterAuraMax'].apply(get_aura_dict_from_str))
        df_hero_quality_growth = df_hero_quality_growth.join(
            df_hero_quality_growth['PvpLimiterTypeAuraMax'].apply(get_type_aura_dict_from_str))

    # 5. 读取天赋成长信息
    global df_hero_talent_growth
    df_hero_talent_growth = read_spec_file('HeroTalentAttribute')
    df_hero_talent_growth = df_hero_talent_growth.drop([0])
    df_hero_talent_growth = df_hero_talent_growth.join(df_hero_talent_growth['Attribute'].apply(get_dict_from_str))
    df_hero_talent_growth = df_hero_talent_growth.drop(['Attribute'], axis=1)

    # 6. 读取装备信息
    global df_equip_property
    df_equip_property = read_spec_file('Equip')
    df_equip_property = df_equip_property.join(df_equip_property['Attribute'].apply(get_dict_from_str))
    df_equip_property = df_equip_property.loc[:, df_equip_property.columns.intersection(['Id', 'AttributeInfo'])]

    # 7. 读取核心研究所信息
    global df_core_property
    df_core_property = read_spec_file('HeroAcademyLevel')
    if a_type == 'pve':
        df_core_property = df_core_property.join(df_core_property['Attribute'].apply(get_dict_from_str))
    else:
        df_core_property = df_core_property.join(df_core_property['PvpAttribute'].apply(get_dict_from_str))
    df_core_property = df_core_property.loc[:, df_core_property.columns.intersection(['Id', 'Level', 'AttributeInfo'])]

    # 7. 读取职阶信息
    global df_job_property
    df_job_property = read_spec_file('HeroJobLevel')
    if a_type == 'pve':
        df_job_property = df_job_property.join(df_job_property['Attribute'].apply(get_dict_from_str))
    else:
        df_job_property = df_job_property.join(df_job_property['PvpAttribute'].apply(get_dict_from_str))
    df_job_property = df_job_property.loc[:, df_job_property.columns.intersection(['Id', 'Job', 'Level',
                                                                                   'AttributeInfo'])]

    # 9. 读取英雄限制器突破信息
    global df_limiter
    df_limiter = read_spec_file('HeroLimiter')
    if a_type == 'pve':
        df_limiter = df_limiter.join(df_limiter['Property'].apply(get_dict_from_str))
        df_limiter = df_limiter.join(df_limiter['Aura'].apply(get_aura_dict_from_str))
        df_limiter = df_limiter.join(df_limiter['TypeAura'].apply(get_type_aura_dict_from_str))
    else:
        df_limiter = df_limiter.join(df_limiter['PvpProperty'].apply(get_dict_from_str))
        df_limiter = df_limiter.join(df_limiter['PvpAura'].apply(get_aura_dict_from_str))
        df_limiter = df_limiter.join(df_limiter['PvpTypeAura'].apply(get_type_aura_dict_from_str))
    df_limiter = df_limiter.loc[:, df_limiter.columns.intersection(['Id', 'Heroid', 'LimiterLevel', 'AttributeInfo',
                                                                    'AuraAttribute', 'TypeAuraAttribute'])]

    # 10. 读取机械核心信息
    global df_mechanical_core
    df_mechanical_core = read_spec_file('MechanicalPowerLevel')
    if a_type == 'pve':
        df_mechanical_core = df_mechanical_core.join(df_mechanical_core['Attribute'].apply(get_dict_from_str))
    else:
        df_mechanical_core = df_mechanical_core.join(df_mechanical_core['PvpAttribute'].apply(get_dict_from_str))
    df_mechanical_core = df_mechanical_core.loc[:, df_mechanical_core.columns.intersection(['Id', 'Heroid', 'Level',
                                                                                            'AttributeInfo'])]

    # 8. 读取战力参数
    global power_params
    df_configs = read_spec_file('Configs')
    power_params = {
        20: get_specific_property(df_configs, 'value', 'key', 'PowerParamHp'),
        21: get_specific_property(df_configs, 'value', 'key', 'PowerParamHp'),
        22: 0,
        23: 0,
        30: get_specific_property(df_configs, 'value', 'key', 'PowerParamAtk'),
        31: get_specific_property(df_configs, 'value', 'key', 'PowerParamAtk'),
        32: 0,
        33: 0,
        40: get_specific_property(df_configs, 'value', 'key', 'PowerParamDef'),
        41: get_specific_property(df_configs, 'value', 'key', 'PowerParamDef'),
        42: 0,
        43: 0,
        50: get_specific_property(df_configs, 'value', 'key', 'PowerParamDmgRes'),
        60: get_specific_property(df_configs, 'value', 'key', 'PowerParamCritRes'),
        70: get_specific_property(df_configs, 'value', 'key', 'PowerParamCrit'),
        140: get_specific_property(df_configs, 'value', 'key', 'PowerParamParry'),
        150: get_specific_property(df_configs, 'value', 'key', 'PowerParamPrecise'),
    }

    print('spec数据读取完毕！')


# ******************************* 特定方法 ******************************

def get_hero_grade_by_level(_level):
    if _level <= 10:
        return 1
    else:
        return min(19, int((_level - 1) / 20) + 2)


def get_hero_equips(_role, _quality):
    # 获取装备id
    return [_role * 1000 + 100 + _quality,
            _role * 1000 + 200 + _quality,
            _role * 1000 + 300 + _quality,
            _role * 1000 + 400 + _quality]


def union_dict(dict_base, dict2, rate=1.0):
    # 合并属性
    for key in dict2.keys():
        dict_base[key] += dict2[key] * rate
    return dict_base


def print_attribute(attr_dict, _head):
    # 打印属性：将属性字典转换为字符串打印
    dict_names = {21: '生命',
                  22: '生命加成',
                  31: '攻击',
                  32: '攻击加成',
                  41: '防御',
                  42: '防御加成',
                  50: '伤害减免',
                  60: '暴击减免',
                  70: '暴击',
                  140: '格挡',
                  150: '精准'}
    desc = _head
    for key in attr_dict.keys():
        desc += dict_names[key] + ',' + str(attr_dict[key]) + ';'
    print(desc)


def get_power(hero_hp, hero_atk, hero_def, hero_crit=0, hero_crit_res=0, hero_precise=0, hero_parry=0, hero_dmg_res=0):
    # 计算战斗力
    return hero_hp * power_hp + hero_atk * power_atk + hero_def * power_def + hero_crit * power_crit + \
           hero_crit_res * power_crit_res + hero_precise * power_precise + hero_parry * power_parry + \
           hero_dmg_res * power_dmg_res


def calculate_power(dict):
    power = 0
    for key in dict.keys():
        power += dict[key] * power_params[key]
    return power

# ******************************* 计算过程 ******************************

def calculate_properties(hp_base, atk_base, def_base, crit_base, property_dict, _hp_m=-1, _atk_m=-1, _def_m=-1,
                         _init=False):
    # 计算最终属性
    if _init:
        hero_hp = hp_base
        hero_atk = atk_base
        hero_def = def_base
        hero_crit = crit_base
        hero_crit_res = 0
        hero_precise = 0
        hero_parry = 0
        hero_dmg_res = 0
    else:
        hero_hp = hp_base * (property_dict[22]) / 10000 + property_dict[21]
        hero_atk = atk_base * (property_dict[32]) / 10000 + property_dict[31]
        hero_def = def_base * (property_dict[42]) / 10000 + property_dict[41]
        hero_crit = property_dict[70]
        hero_crit_res = property_dict[60]
        hero_precise = property_dict[150]
        hero_parry = property_dict[140]
        hero_dmg_res = property_dict[50]

    # 计算战斗力
    power = get_power(hero_hp, hero_atk, hero_def, hero_crit, hero_crit_res, hero_precise, hero_parry, hero_dmg_res)
    hero_dict = {
        'hp': hero_hp,
        'atk': hero_atk,
        'def': hero_def,
        'crit': hero_crit,
        'crit_res': hero_crit_res,
        'precise': hero_precise,
        'parry': hero_parry,
        'dmg_res': hero_dmg_res,
        'power': power,
    }
    return hero_dict


def calculate_base_percentage_property(_base, _p):
    # 计算基础百分比属性
    _p[21] += _base[20] * _p[22]
    _p[31] += _base[30] * _p[32]
    _p[41] += _base[40] * _p[42]
    return _p


def calculate_total_percentage_property(_p):
    # 计算总百分比属性
    return _p


# 计算英雄基础属性
def get_hero_base_property(_id, _quality, _level, _lv_enhance):

    # 角色初始属性
    hp_init = get_specific_property(df_hero, 'HpBase', 'Id', _id)
    atk_init = get_specific_property(df_hero, 'AtkBase', 'Id', _id)
    def_init = get_specific_property(df_hero, 'DefBase', 'Id', _id)
    crit_init = get_specific_property(df_hero, 'CritBase', 'Id', _id)
    if test_mode:
        print('初始属性：生命 = %f,攻击 = %f,防御 = %f,暴击 = %f' % (hp_init, atk_init, def_init, crit_init))

    # 角色品质属性
    hp_qua_per = get_specific_property(df_hero_quality_growth, 'HpParam', 'HeroId', _id, 'QualityLevel', _quality)
    atk_qua_per = get_specific_property(df_hero_quality_growth, 'AtkParam', 'HeroId', _id, 'QualityLevel', _quality)
    def_qua_per = get_specific_property(df_hero_quality_growth, 'DefParam', 'HeroId', _id, 'QualityLevel', _quality)

    if test_mode:
        print('品质成长：生命加成 = %f,攻击加成 = %f,防御加成 = %f' % (hp_qua_per, atk_qua_per, def_qua_per))

    hp_qua_inc = get_specific_property(df_hero_quality_growth, 'HpInc', 'HeroId', _id, 'QualityLevel', _quality)
    atk_qua_inc = get_specific_property(df_hero_quality_growth, 'AtkInc', 'HeroId', _id, 'QualityLevel', _quality)
    def_qua_inc = get_specific_property(df_hero_quality_growth, 'DefInc', 'HeroId', _id, 'QualityLevel', _quality)

    if test_mode:
        print('品质成长：生命 = %f,攻击 = %f,防御 = %f' % (hp_qua_inc, atk_qua_inc, def_qua_inc))
    # 角色等级成长
    hp_lv_inc = get_specific_property(df_hero_lv_growth, 'HpInc', 'Level', _level, 'EnhancePeriod', _lv_enhance)
    atk_lv_inc = get_specific_property(df_hero_lv_growth, 'AtkInc', 'Level', _level, 'EnhancePeriod', _lv_enhance)
    def_lv_inc = get_specific_property(df_hero_lv_growth, 'DefInc', 'Level', _level, 'EnhancePeriod', _lv_enhance)
    if test_mode:
        print('等级成长：生命 = %f,攻击 = %f,防御 = %f' % (hp_lv_inc, atk_lv_inc, def_lv_inc))

    # 角色品阶属性
    _grade = get_hero_grade_by_level(_level)
    hp_grade_inc = get_specific_property(df_hero_grade_growth, 'HpInc', 'HeroId', _id, 'GradeLevel', _grade)
    atk_grade_inc = get_specific_property(df_hero_grade_growth, 'AtkInc', 'HeroId', _id, 'GradeLevel', _grade)
    def_grade_inc = get_specific_property(df_hero_grade_growth, 'DefInc', 'HeroId', _id, 'GradeLevel', _grade)
    if test_mode:
        print('品阶成长：生命 = %f,攻击 = %f,防御 = %f' % (hp_grade_inc, atk_grade_inc, def_grade_inc))

    # 基础属性汇总
    hp_base = hp_init + hp_lv_inc * hp_qua_per / 10000 + hp_qua_inc + hp_grade_inc
    atk_base = atk_init + atk_lv_inc * atk_qua_per / 10000 + atk_qua_inc + atk_grade_inc
    def_base = def_init + def_lv_inc * def_qua_per / 10000 + def_qua_inc + def_grade_inc
    crit_base = crit_init

    return hp_base, atk_base, def_base, crit_base


def get_hero_equip_property(_id, _quality, _level, _lv_enhance, _e_qua, _e_enhance):
    # 角色装备属性
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    if _e_qua > 0:
        _role = get_specific_property(df_hero, 'Role', 'Id', _id)
        equip_list = get_hero_equips(_role, _e_qua)
        for equip in equip_list:
            equip_attr = get_specific_property(df_equip_property, 'AttributeInfo', 'Id', equip)

            # 默认规则：如果有强化，则默认该装备有类型加成，否则无加成
            if _e_enhance > 0:
                property_dict = union_dict(property_dict, equip_attr, 1.3 + _e_enhance / 10)
            else:
                property_dict = union_dict(property_dict, equip_attr, 1)
    return property_dict


def get_hero_talent_property(_id, _talent, _base):
    # 角色天赋
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    if _talent >= 0:
        talent_attr = get_specific_property(df_hero_talent_growth, 'AttributeInfo', 'HeroId', _id, 'TalentLevel',
                                            _talent)

        property_dict = union_dict(property_dict, talent_attr)
        property_dict = calculate_base_percentage_property(_base, property_dict)

    return property_dict


def get_hero_core_property(_core):
    # 研究所核心
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    if _core > 0:
        core_attr = get_specific_property(df_core_property, 'AttributeInfo', 'Id', _core)
        property_dict = union_dict(property_dict, core_attr)
    return property_dict


def get_hero_job_property(_id, _job):
    # 研究所职阶
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    if _job > 0:
        job = get_specific_property(df_hero, 'Job', 'Id', _id)
        job_attr = get_specific_property(df_job_property, 'AttributeInfo', 'Level', _job, 'Job', job)
        property_dict = union_dict(property_dict, job_attr)
    return property_dict


def get_hero_job_connect_property(_id, _job):
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    # if _mechanical > 0:
    #     pass


def get_mechanical_property(_id, _mechanical, _base):
    # 职阶核心
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    if _mechanical > 0:
        mechanical_attr = get_specific_property(df_mechanical_core, 'AttributeInfo', 'HeroId', _id, 'Level', _mechanical)
        property_dict = union_dict(property_dict, mechanical_attr)
        property_dict = calculate_base_percentage_property(_base, property_dict)
    return property_dict


def get_hero_limiter_property(_id, _quality, _level, _lv_enhance, _limiter):
    print('\t正在处理角色：%d' % _id)
    hp_base, atk_base, def_base, crit_base = get_hero_base_property(_id, _quality, _level, _lv_enhance)
    property_dict = {21: 0, 22: 0, 31: 0, 32: 0, 41: 0, 42: 0, 50: 0, 60: 0, 70: 0, 140: 0, 150: 0}
    if _limiter > 0:
        limiter_attr = get_specific_property(df_limiter, 'AttributeInfo', 'LimiterLevel', _limiter, 'Heroid', _id)
        property_dict = union_dict(property_dict, limiter_attr)
    hp_max = get_specific_property(df_hero_quality_growth, '21', 'HeroId', _id, 'QualityLevel', _quality)
    atk_max = get_specific_property(df_hero_quality_growth, '31', 'HeroId', _id, 'QualityLevel', _quality)
    def_max = get_specific_property(df_hero_quality_growth, '41', 'HeroId', _id, 'QualityLevel', _quality)
    return calculate_properties(hp_base, atk_base, def_base, crit_base, property_dict, 1, hp_max, atk_max, def_max)


def get_hero_properties(_id, _quality, _level, _lv_enhance, _e_qua, _e_enhance, _talent, _core, _job, _limiter,
                        _mechanical, _collect):
    print('\t正在处理角色：%d' % _id)

    # 0 初始化属性
    properties = {20: 0,
                  21: 0,
                  22: 0,
                  23: 0,
                  30: 0,
                  31: 0,
                  32: 0,
                  33: 0,
                  40: 0,
                  41: 0,
                  42: 0,
                  43: 0,
                  50: 0,
                  60: 0,
                  70: 0,
                  140: 0,
                  150: 0,
                  }
    powers = {}

    # 基础属性
    hp_base, atk_base, def_base, crit_base = get_hero_base_property(_id, _quality, _level, _lv_enhance)
    property_base = {20:hp_base, 30:atk_base, 40:def_base, 70:crit_base}
    properties = union_dict(properties, property_base)

    power_base = calculate_power(property_base)
    powers.add('base', power_base)

    # 装备属性
    property_equip = get_hero_equip_property(_id, _quality, _level, _lv_enhance, _e_qua, _e_enhance)
    properties = union_dict(properties, property_equip)

    power_equip = calculate_power(property_equip)
    powers.add('equip', power_equip)

    # 天赋属性
    property_talent = get_hero_talent_property(_id, _talent, property_base)
    properties = union_dict(properties, property_talent)

    power_talent = calculate_power(property_talent)
    powers.add('talent', power_talent)

    # 研究所核心
    property_core = get_hero_core_property(_core)
    properties = union_dict(properties, property_core)

    power_core = calculate_power(property_core)
    powers.add('core', power_core)

    # 研究所职阶
    property_job = get_hero_job_property(_id, _job)
    properties = union_dict(properties, property_job)

    power_job = calculate_power(property_job)
    powers.add('job', power_job)

    # todo
    property_job_connect = {}

    # 机械核心
    property_mechanical = get_mechanical_property(_id, _mechanical, property_base)
    properties = union_dict(property_base, property_mechanical)

    power_mechanical = calculate_power(property_mechanical)
    powers.add('mechanical', power_mechanical)

    property_limiter = {}
    property_collect = {}

    pass


# ******************************* 程序初始化 ******************************

os.system('clear')
print(
        '*' * 50 + '\n' + '*' * 50 + '\n' + '\t\t\t\t欢迎使用OPM集成脚本！\n'
        + '\t\t\t\t\t\t\t\t----Made by CnSky\n' + '*' * 50 + '\n' + '*' * 50 + '\n')
print('Initializing Data...')

test_mode = False
a_type = 'pve'

# 1. 设定Spec版本号
set_version_path()
# 2. 英雄基础信息
df_hero = pd.DataFrame()
# 3. 等级成长信息
df_hero_lv_growth = pd.DataFrame()
# 4. 等级突破成长信息
df_hero_grade_growth = pd.DataFrame()
# 5. 品质成长信息
df_hero_quality_growth = pd.DataFrame()
# 6. 天赋成长信息
df_hero_talent_growth = pd.DataFrame()
# 7. 装备信息
df_equip_property = pd.DataFrame()
# 8. 核心研究所信息
df_core_property = pd.DataFrame()
# 9. 职阶信息
df_job_property = pd.DataFrame()
# 10. 职阶连携信息
df_job_connect = pd.DataFrame()
# 11. 机械核心信息
df_mechanical_core = pd.DataFrame()
# 12. 限制器突破信息
df_limiter = pd.DataFrame()
# 13. 战力参数
power_params = {}

