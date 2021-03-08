import save_hero_info as sv
import pandas as pd
import os


def compare_version(v1, v2):
    """
    比较并返回较新的版本号
    :param v1:
    :param v2:
    :return:
    """
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
    """
    获取spec路径
    :return:
    """
    _p = os.path.abspath('..') + "/specs/"
    folders = os.listdir(_p)
    current_version = folders[0]
    for folder in folders:
        current_version = compare_version(current_version, folder)
    return _p + current_version + '/xlsx_origin/'


def read_spec_file(file_name):
    """
    读取spec表并进行统一处理
    :param file_name:
    :return:
    """
    # 以第3行为标题读取数据
    _df = pd.read_excel(path + file_name + '.xlsx', header=2, sheet_name=file_name)
    # 删除空行
    _df.dropna(axis=0, how='all')
    # 删除中文标示
    _df = _df.drop([0])
    # 重置序号后返回
    return _df.reset_index()


def get_specific_property(_df, target_name, column_name1, value1, column_name2='', value2=None):
    """
    从DataFrame中获取指定条件的值，最多限定两个条件
    :param _df:
    :param target_name:
    :param column_name1:
    :param value1:
    :param column_name2:
    :param value2:
    :return:
    """
    if column_name2 == '':
        n = _df[_df[column_name1] == value1].index.values.astype(int)[0]
    else:
        n = _df[(_df[column_name1] == value1) & (_df[column_name2] == value2)].index.values.astype(int)[0]
    return _df.loc[n, target_name]


def get_split_values(s):
    ss = s.split(';')
    a = 0
    b = 0
    c = 0
    for x in ss:
        sss = x.split(',')
        if sss[0] == '21':
            a = int(sss[1])
        if sss[0] == '31':
            b = int(sss[1])
        if sss[0] == '41':
            c = int(sss[1])
    return a, b, c


def get_split_values_and_per(s):
    ss = s.split(';')
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    for x in ss:
        sss = x.split(',')
        if sss[0] == '21':
            a = int(sss[1])
        if sss[0] == '31':
            b = int(sss[1])
        if sss[0] == '41':
            c = int(sss[1])
        if sss[0] == '22':
            d = int(sss[1])
        if sss[0] == '32':
            e = int(sss[1])
        if sss[0] == '42':
            f = int(sss[1])
    return a, b, c, d, e, f


def get_split_talent_value(s):
    ss = s.split(';')
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0
    for x in ss:
        sss = x.split(',')
        if sss[0] == '22':
            a = int(sss[1])
        if sss[0] == '32':
            b = int(sss[1])
        if sss[0] == '42':
            c = int(sss[1])
        if sss[0] == '70':
            d = int(sss[1])
        if sss[0] == '60':
            e = int(sss[1])
        if sss[0] == '150':
            f = int(sss[1])
        if sss[0] == '140':
            g = int(sss[1])
        if sss[0] == '50':
            h = int(sss[1])
    return a, b, c, d, e, f, g, h


path = ''
path = set_version_path()
df_hero_info = pd.read_excel('design/hero_design.xlsx', index_col=0, header=0)

hero_list = [1, 2, 8, 10, 11, 12, 13, 18, 19, 20, 21, 23, 24, 25, 26, 27, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42,
             43, 44, 45, 46, 49, 51, 60, 61, 62, 63, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 100,
             101, 102, 103]

# hero_list = [ 92, 93, 94, 95, 96, 97, 98, 100,
#              101, 102, 103]

for _id in hero_list:

    # 加载英雄基本信息
    df_hero = read_spec_file('Hero')
    df_hero = df_hero.loc[:, df_hero.columns.intersection(
        ['Id', 'Rarity', 'Type', 'Role', 'HpBase', 'AtkBase', 'DefBase', 'CritBase', 'Job'])]
    _name = df_hero_info.loc[_id, '_name']
    print('正在处理 ' + _name)

    _camp = get_specific_property(df_hero, 'Type', 'Id', _id)
    _profession = get_specific_property(df_hero, 'Role', 'Id', _id)
    _job = get_specific_property(df_hero, 'Job', 'Id', _id) + 30000
    _hp_init = get_specific_property(df_hero, 'HpBase', 'Id', _id)
    _atk_init = get_specific_property(df_hero, 'AtkBase', 'Id', _id)
    _def_init = get_specific_property(df_hero, 'DefBase', 'Id', _id)

    sv.save_hero_basic_info(_id, _name, _camp, _profession, _job, _hp_init, _atk_init, _def_init)

    # 加载品阶成长信息
    df_hero_grade_growth = read_spec_file('HeroGradeProperty')
    hp_grade = []
    atk_grade = []
    def_grade = []
    for i in range(0, 20):
        v = get_specific_property(df_hero_grade_growth, 'HpInc', 'HeroId', _id, 'GradeLevel', i + 1)
        hp_grade.append(v)
        v = get_specific_property(df_hero_grade_growth, 'AtkInc', 'HeroId', _id, 'GradeLevel', i + 1)
        atk_grade.append(v)
        v = get_specific_property(df_hero_grade_growth, 'DefInc', 'HeroId', _id, 'GradeLevel', i + 1)
        def_grade.append(v)
    sv.save_hero_grade_growth(_id, hp_grade, atk_grade, def_grade)

    # 加载品质成长信息
    df_hero_quality_growth = read_spec_file('HeroQualityProperty')
    hp_quality_per = []
    atk_quality_per = []
    def_quality_per = []
    hp_quality_value = []
    atk_quality_value = []
    def_quality_value = []

    value_max_pve = []
    hp1 = []
    atk1 = []
    def1 = []
    aura_max_pve = []
    hp2 = []
    atk2 = []
    def2 = []
    type_aura_max_pve = []
    hp3 = []
    atk3 = []
    def3 = []

    value_max_pvp = []
    hp4 = []
    atk4 = []
    def4 = []
    aura_max_pvp = []
    hp5 = []
    atk5 = []
    def5 = []
    type_aura_max_pvp = []
    hp6 = []
    atk6 = []
    def6 = []

    for i in range(0, 16):
        v = get_specific_property(df_hero_quality_growth, 'HpParam', 'HeroId', _id, 'QualityLevel', i + 1)
        hp_quality_per.append(v)
        v = get_specific_property(df_hero_quality_growth, 'AtkParam', 'HeroId', _id, 'QualityLevel', i + 1)
        atk_quality_per.append(v)
        v = get_specific_property(df_hero_quality_growth, 'DefParam', 'HeroId', _id, 'QualityLevel', i + 1)
        def_quality_per.append(v)
        v = get_specific_property(df_hero_quality_growth, 'HpInc', 'HeroId', _id, 'QualityLevel', i + 1)
        hp_quality_value.append(v)
        v = get_specific_property(df_hero_quality_growth, 'AtkInc', 'HeroId', _id, 'QualityLevel', i + 1)
        atk_quality_value.append(v)
        v = get_specific_property(df_hero_quality_growth, 'DefInc', 'HeroId', _id, 'QualityLevel', i + 1)
        def_quality_value.append(v)

        v = get_specific_property(df_hero_quality_growth, 'LimiterPropertyMax', 'HeroId', _id, 'QualityLevel', i + 1)
        value_max_pve.append(v)
        _hp, _atk, _def = get_split_values(v)
        hp1.append(_hp)
        atk1.append(_atk)
        def1.append(_def)
        v = get_specific_property(df_hero_quality_growth, 'LimiterAuraMax', 'HeroId', _id, 'QualityLevel', i + 1)
        aura_max_pve.append(v)
        _hp, _atk, _def = get_split_values(v)
        hp2.append(_hp)
        atk2.append(_atk)
        def2.append(_def)
        v = get_specific_property(df_hero_quality_growth, 'LimiterTypeAuraMax', 'HeroId', _id, 'QualityLevel', i + 1)
        type_aura_max_pve.append(v)
        _hp, _atk, _def = get_split_values(v)
        hp3.append(_hp)
        atk3.append(_atk)
        def3.append(_def)
        v = get_specific_property(df_hero_quality_growth, 'PvpLimiterPropertyMax', 'HeroId', _id, 'QualityLevel', i + 1)
        value_max_pvp.append(v)
        _hp, _atk, _def = get_split_values(v)
        hp4.append(_hp)
        atk4.append(_atk)
        def4.append(_def)
        v = get_specific_property(df_hero_quality_growth, 'PvpLimiterAuraMax', 'HeroId', _id, 'QualityLevel', i + 1)
        aura_max_pvp.append(v)
        _hp, _atk, _def = get_split_values(v)
        hp5.append(_hp)
        atk5.append(_atk)
        def5.append(_def)
        v = get_specific_property(df_hero_quality_growth, 'PvpLimiterTypeAuraMax', 'HeroId', _id, 'QualityLevel', i + 1)
        type_aura_max_pvp.append(v)
        _hp, _atk, _def = get_split_values(v)
        hp6.append(_hp)
        atk6.append(_atk)
        def6.append(_def)

    sv.save_hero_quality_growth(_id, hp_quality_per, atk_quality_per, def_quality_per,
                                hp_quality_value, atk_quality_value, def_quality_value)
    sv.save_hero_quality_max_value(_id, hp1, atk1, def1, hp4, atk4, def4, hp2, atk2, def2, hp5, atk5, def5,
                                   hp3, atk3, def3, hp6, atk6, def6)

    # 加载天赋信息
    df_hero_talent_growth = read_spec_file('HeroTalentAttribute')
    talent_lv = 41 if _camp == 5 else 31
    hp_per_talent = []
    atk_per_talent = []
    def_per_talent = []
    crit_talent = []
    crit_res_talent = []
    precise_talent = []
    parry_talent = []
    dmg_res_talent = []
    for i in range(0, talent_lv):
        v = get_specific_property(df_hero_talent_growth, 'Attribute', 'HeroId', _id, 'TalentLevel', i)
        a, b, c, d, e, f, g, h = get_split_talent_value(v)
        hp_per_talent.append(a/100)
        atk_per_talent.append(b/100)
        def_per_talent.append(c/100)
        crit_talent.append(d)
        crit_res_talent.append(e)
        precise_talent.append(f)
        parry_talent.append(g)
        dmg_res_talent.append(h)
    sv.save_hero_talent_growth(_id, talent_lv, hp_per_talent, atk_per_talent, def_per_talent,
                               crit_talent, crit_res_talent, precise_talent, parry_talent, dmg_res_talent)

    # 加载机械核心信息
    df_mechanical_core = read_spec_file('MechanicalPowerLevel')
    hp_me_pve = []
    atk_me_pve = []
    def_me_pve = []
    hp_me_pvp = []
    atk_me_pvp = []
    def_me_pvp = []

    for i in range(0, 30):
        v = get_specific_property(df_mechanical_core, 'Attribute', 'HeroId', _id, 'Level', i + 1)
        a, b, c = get_split_values(v)
        hp_me_pve.append(a)
        atk_me_pve.append(b)
        def_me_pve.append(c)
        v = get_specific_property(df_mechanical_core, 'PvpAttribute', 'HeroId', _id, 'Level', i + 1)
        a, b, c = get_split_values(v)
        hp_me_pvp.append(a)
        atk_me_pvp.append(b)
        def_me_pvp.append(c)
    sv.save_hero_mechanical_power(_id, hp_me_pve, atk_me_pve, def_me_pve, hp_me_pvp, atk_me_pvp, def_me_pvp)

    # 加载限制器信息

    df_limiter = read_spec_file('HeroLimiter')
    hp_pve_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pve_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pve_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pve_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pve_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pve_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    atk_pve_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pve_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pve_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pve_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pve_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pve_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def_pve_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pve_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pve_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pve_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pve_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pve_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    hp_pvp_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pvp_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pvp_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pvp_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pvp_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hp_pvp_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    atk_pvp_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pvp_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pvp_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pvp_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pvp_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    atk_pvp_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def_pvp_v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pvp_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pvp_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pvp_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pvp_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def_pvp_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    has_hero = (_id in df_limiter['Heroid'].tolist())
    if has_hero:
        for i in range(0, 10):
            v = get_specific_property(df_limiter, 'Property', 'Heroid', _id, 'LimiterLevel', i + 1)
            a, b, c, d, e, f = get_split_values_and_per(v)
            hp_pve_v[i] = a
            atk_pve_v[i] = b
            def_pve_v[i] = c
            hp_pve_per[i] = d
            atk_pve_per[i] = e
            def_pve_per[i] = f

            v = get_specific_property(df_limiter, 'Aura', 'Heroid', _id, 'LimiterLevel', i + 1)
            a, b, c, d, e, f = get_split_values_and_per(v)
            hp_pve_aura[i] = a
            atk_pve_aura[i] = b
            def_pve_aura[i] = c
            hp_pve_aura_per[i] = d
            atk_pve_aura_per[i] = e
            def_pve_aura_per[i] = f

            v = get_specific_property(df_limiter, 'TypeAura', 'Heroid', _id, 'LimiterLevel', i + 1)
            a, b, c, d, e, f = get_split_values_and_per(v)
            hp_pve_type_aura[i] = a
            atk_pve_type_aura[i] = b
            def_pve_type_aura[i] = c
            hp_pve_type_aura_per[i] = d
            atk_pve_type_aura_per[i] = e
            def_pve_type_aura_per[i] = f

            v = get_specific_property(df_limiter, 'PvpProperty', 'Heroid', _id, 'LimiterLevel', i + 1)
            a, b, c, d, e, f = get_split_values_and_per(v)
            hp_pvp_v[i] = a
            atk_pvp_v[i] = b
            def_pvp_v[i] = c
            hp_pvp_per[i] = d
            atk_pvp_per[i] = e
            def_pvp_per[i] = f

            v = get_specific_property(df_limiter, 'PvpAura', 'Heroid', _id, 'LimiterLevel', i + 1)
            a, b, c, d, e, f = get_split_values_and_per(v)
            hp_pvp_aura[i] = a
            atk_pvp_aura[i] = b
            def_pvp_aura[i] = c
            hp_pvp_aura_per[i] = d
            atk_pvp_aura_per[i] = e
            def_pvp_aura_per[i] = f

            v = get_specific_property(df_limiter, 'PvpTypeAura', 'Heroid', _id, 'LimiterLevel', i + 1)
            a, b, c, d, e, f = get_split_values_and_per(v)
            hp_pvp_type_aura[i] = a
            atk_pvp_type_aura[i] = b
            def_pvp_type_aura[i] = c
            hp_pvp_type_aura_per[i] = d
            atk_pvp_type_aura_per[i] = e
            def_pvp_type_aura_per[i] = f
    sv.save_hero_limiter_growth(_id, hp_pve_v, hp_pve_per, hp_pve_aura, hp_pve_aura_per, hp_pve_type_aura,
                                hp_pve_type_aura_per, hp_pvp_v, hp_pvp_per, hp_pvp_aura, hp_pvp_aura_per,
                                hp_pvp_type_aura, hp_pvp_type_aura_per, atk_pve_v, atk_pve_per, atk_pve_aura,
                                atk_pve_aura_per, atk_pve_type_aura, atk_pve_type_aura_per, atk_pvp_v, atk_pvp_per,
                                atk_pvp_aura, atk_pvp_aura_per, atk_pvp_type_aura, atk_pvp_type_aura_per, def_pve_v,
                                def_pve_per, def_pve_aura, def_pve_aura_per, def_pve_type_aura, def_pve_type_aura_per,
                                def_pvp_v, def_pvp_per, def_pvp_aura, def_pvp_aura_per, def_pvp_type_aura,
                                def_pvp_type_aura_per)
