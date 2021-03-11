import pandas as pd
import save_hero_info as sv
import opm_property_tools as tools
import load_hero_info as ld


hero_list = [102]

# 限制器成长参数
LIMITER_PVE_VALUE_PARAM = [0.20799999792, 0.271, 0.2492, 0.231, 0.2018, 0.1606, 0.1237, 0.06375, 0.03305, 0.0196]
LIMITER_PVE_AURA_PARAM = [0.20799999792, 0.271, 0.2492, 0.231, 0.2018, 0.1606, 0.1237, 0.06375, 0.03305, 0.0196]
LIMITER_PVE_TYPE_AURA_PARAM = [0.10399999896, 0.1355, 0.1246, 0.1155, 0.1009, 0.0803, 0.06185, 0.031875, 0.016525,
                               0.0098]
LIMITER_PVP_VALUE_PARAM = [0.02, 0.0202, 0.0204, 0.0206, 0.0208, 0.021, 0.0212, 0.0214, 0.0215, 0.0215]
LIMITER_PVP_AURA_PARAM = [0.02, 0.0202, 0.0204, 0.0206, 0.0208, 0.021, 0.0212, 0.0214, 0.0215, 0.0215]
LIMITER_PVP_TYPE_AURA_PARAM = [0.01, 0.0101, 0.0102, 0.0103, 0.0104, 0.0105, 0.0106, 0.0107, 0.01075, 0.01075]

# 读取配置
df_hero = pd.read_excel('design/hero_design.xlsx', index_col=0, header=0)
df_level_growth = pd.read_excel('design/level_growth.xlsx', index_col=0, header=0)


def cal_property(_levels, _qualities, per_hp=1.0, per_atk=1.0, per_def=1.0, _key_lv=True):
    _hp_base = {}
    _atk_base = {}
    _def_base = {}
    for j in range(0, len(_levels)):
        _real_lv = tools.get_real_level(_levels[j], 0)
        _lv_growth_hp = df_level_growth.loc[_real_lv, '_hp_inc']
        _lv_growth_atk = df_level_growth.loc[_real_lv, '_atk_inc']
        _lv_growth_def = df_level_growth.loc[_real_lv, '_def_inc']

        _quality = _qualities[j]
        _quality_hp_per = hp_quality_per[_quality - 1]
        _quality_atk_per = atk_quality_per[_quality - 1]
        _quality_def_per = def_quality_per[_quality - 1]
        _quality_hp_value = hp_quality_value[_quality - 1]
        _quality_atk_value = atk_quality_value[_quality - 1]
        _quality_def_value = def_quality_value[_quality - 1]

        _grade = tools.get_grade(_levels[j])
        _grade_hp_value = hp_grade_value[_grade - 1]
        _grade_atk_value = atk_grade_value[_grade - 1]
        _grade_def_value = def_grade_value[_grade - 1]

        if _key_lv:
            _hp_base[_levels[j]] = (hp_init + _lv_growth_hp * _quality_hp_per / 10000 +
                                    _quality_hp_value + _grade_hp_value) * per_hp
            _atk_base[_levels[j]] = (atk_init + _lv_growth_atk * _quality_atk_per / 10000 +
                                     _quality_atk_value + _grade_atk_value) * per_atk
            _def_base[_levels[j]] = (def_init + _lv_growth_def * _quality_def_per / 10000 +
                                     _quality_def_value + _grade_def_value) * per_def
        else:
            _hp_base[_qualities[j] - 1] = (hp_init + _lv_growth_hp * _quality_hp_per / 10000 +
                                           _quality_hp_value + _grade_hp_value) * per_hp
            _atk_base[_qualities[j] - 1] = (atk_init + _lv_growth_atk * _quality_atk_per / 10000 +
                                            _quality_atk_value + _grade_atk_value) * per_atk
            _def_base[_qualities[j] - 1] = (def_init + _lv_growth_def * _quality_def_per / 10000 +
                                            _quality_def_value + _grade_def_value) * per_def
    return _hp_base, _atk_base, _def_base


def get_offset_type(a, b, c):
    a = float(a)
    b = float(b)
    c = float(c)
    if a > 0 and b > 0 and c > 0:
        return 'all'
    elif a > 0 and b > 0:
        return 'hp_atk'
    elif a > 0 and c > 0:
        return 'hp_def'
    elif b > 0 and c > 0:
        return 'atk_def'
    elif a > 0:
        return 'hp'
    elif b > 0:
        return 'atk'
    elif c > 0:
        return 'def'
    else:
        return 'none'


for i in hero_list:
    # 角色基本信息
    _id, _name, _camp, _profession, _job, hp_init, atk_init, def_init, crit_init = ld.load_hero_basic_info(i)
    # 品质成长
    x = ld.load_hero_quality_growth(_id)
    hp_quality_per = x[0]
    atk_quality_per = x[1]
    def_quality_per = x[2]
    hp_quality_value = x[3]
    atk_quality_value = x[4]
    def_quality_value = x[5]
    # 品阶成长
    hp_grade_value, atk_grade_value, def_grade_value = ld.load_hero_grade_growth(_id)

    # 计算限制器PVE属性及光环
    # 0.读取偏移数据
    v = df_hero.loc[_id, '_limiter_offset']
    _complete_param = 1.5 if _camp == 5 else 1.0    # 用于弥补全能角色基础属性较低导致的限制器属性偏低的问题
    # 1. 计算标准等级基础属性
    hero_level_list = [160, 180, 200, 220, 240, 260, 280, 320, 360, 400]
    hero_quality_list = [9, 10, 11, 12, 13, 14, 15, 16, 16, 16, 16, 16, 16]
    hp_base, atk_base, def_base = cal_property(hero_level_list, hero_quality_list)

    # 2. 计算限制器基础属性
    df_limiter = pd.read_excel('design/limiter_offset.xlsx', sheet_name='all', index_col=0, header=0)
    hp_limiter = []
    atk_limiter = []
    def_limiter = []
    hp_limiter_per = [40, 80, 120, 160, 200, 240, 280, 315, 335, 350]
    atk_limiter_per = [40, 80, 120, 160, 200, 240, 280, 315, 335, 350]
    def_limiter_per = [40, 80, 120, 160, 200, 240, 280, 315, 335, 350]
    _level_list_1 = [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]
    _quality_list_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    _hp_1 = df_limiter.loc[v, '_hp']
    _atk_1 = df_limiter.loc[v, '_atk']
    _def_1 = df_limiter.loc[v, '_def']

    for j in range(0, 10):
        _hp_3 = hp_base[hero_level_list[j]]
        hp_limiter.append(int(_hp_3 * _hp_1 * LIMITER_PVE_VALUE_PARAM[j]))
        hp_limiter_per[j] = int(hp_limiter_per[j] * _hp_1 * _complete_param)

        _atk_3 = atk_base[hero_level_list[j]]
        atk_limiter.append(int(_atk_3 * _atk_1 * LIMITER_PVE_VALUE_PARAM[j]))
        atk_limiter_per[j] = int(atk_limiter_per[j] * _atk_1 * _complete_param)

        _def_3 = def_base[hero_level_list[j]]
        def_limiter.append(int(_def_3 * _def_1 * LIMITER_PVE_VALUE_PARAM[j]))
        def_limiter_per[j] = int(def_limiter_per[j] * _def_1 * _complete_param)

    # 优化属性值
    for j in range(0, 10):
        hp_limiter[j] = int((j + 1) / 10 * hp_limiter[9] * _complete_param)
        atk_limiter[j] = int((j + 1) / 10 * atk_limiter[9] * _complete_param)
        def_limiter[j] = int((j + 1) / 10 * def_limiter[9] * _complete_param)

    hp_max, atk_max, def_max = cal_property(_level_list_1, _quality_list_1, hp_limiter_per[9] / 10000,
                                            atk_limiter_per[9] / 10000, def_limiter_per[9] / 10000, False)

    # 3. 计算限制器全体光环
    _hp_4 = df_hero.loc[_id, '_aura_hp']
    _atk_4 = df_hero.loc[_id, '_aura_atk']
    _def_4 = df_hero.loc[_id, '_aura_def']
    _type = get_offset_type(_hp_4, _atk_4, _def_4)
    df_limiter = pd.read_excel('design/limiter_offset.xlsx', sheet_name=_type, index_col=0, header=0)

    hp_limiter_aura = []
    atk_limiter_aura = []
    def_limiter_aura = []
    hp_limiter_aura_per = [40, 80, 120, 160, 200, 240, 280, 315, 335, 350]
    atk_limiter_aura_per = [40, 80, 120, 160, 200, 240, 280, 315, 335, 350]
    def_limiter_aura_per = [40, 80, 120, 160, 200, 240, 280, 315, 335, 350]

    _hp_2 = df_limiter.loc[v, '_hp']
    _atk_2 = df_limiter.loc[v, '_atk']
    _def_2 = df_limiter.loc[v, '_def']
    for j in range(0, 10):
        _hp_3 = hp_base[hero_level_list[j]]
        hp_limiter_aura.append(int(_hp_3 * _hp_2 * LIMITER_PVE_AURA_PARAM[j]))
        hp_limiter_aura_per[j] = int(hp_limiter_aura_per[j] * _hp_4 * _hp_1)
        _atk_3 = atk_base[hero_level_list[j]]
        atk_limiter_aura.append(int(_atk_3 * _atk_2 * LIMITER_PVE_AURA_PARAM[j]))
        atk_limiter_aura_per[j] = int(atk_limiter_aura_per[j] * _atk_4 * _atk_1)
        _def_3 = def_base[hero_level_list[j]]
        def_limiter_aura.append(int(_def_3 * _def_2 * LIMITER_PVE_AURA_PARAM[j]))
        def_limiter_aura_per[j] = int(def_limiter_aura_per[j] * _def_4 * _def_1)

    # 优化属性值
    for j in range(0, 10):
        hp_limiter_aura[j] = int((j + 1) / 10 * hp_limiter_aura[9])
        atk_limiter_aura[j] = int((j + 1) / 10 * atk_limiter_aura[9])
        def_limiter_aura[j] = int((j + 1) / 10 * def_limiter_aura[9])

    hp_max_aura, atk_max_aura, def_max_aura = cal_property(_level_list_1, _quality_list_1,
                                                           hp_limiter_aura_per[9] / 10000,
                                                           atk_limiter_aura_per[9] / 10000,
                                                           def_limiter_aura_per[9] / 10000, False)

    # 3. 计算限制器阵营光环
    _hp_4 = df_hero.loc[_id, '_type_aura_hp']
    _atk_4 = df_hero.loc[_id, '_type_aura_atk']
    _def_4 = df_hero.loc[_id, '_type_aura_def']
    _type = get_offset_type(_hp_4, _atk_4, _def_4)

    if _type == 'none':
        hp_limiter_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        atk_limiter_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        def_limiter_type_aura = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hp_limiter_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        atk_limiter_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        def_limiter_type_aura_per = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hp_max_type_aura, atk_max_type_aura, def_max_type_aura = cal_property(_level_list_1, _quality_list_1, 0, 0, 0,
                                                                              False)
    else:
        df_limiter = pd.read_excel('design/limiter_offset.xlsx', sheet_name=_type, index_col=0, header=0)
        hp_limiter_type_aura = []
        atk_limiter_type_aura = []
        def_limiter_type_aura = []
        hp_limiter_type_aura_per = [20, 40, 60, 80, 100, 120, 140, 157, 167, 175]
        atk_limiter_type_aura_per = [20, 40, 60, 80, 100, 120, 140, 157, 167, 175]
        def_limiter_type_aura_per = [20, 40, 60, 80, 100, 120, 140, 157, 167, 175]

        _hp_2 = df_limiter.loc[v, '_hp']
        _atk_2 = df_limiter.loc[v, '_atk']
        _def_2 = df_limiter.loc[v, '_def']
        for j in range(0, 10):
            _hp_3 = hp_base[hero_level_list[j]]
            hp_limiter_type_aura.append(int(_hp_3 * _hp_2 * LIMITER_PVE_TYPE_AURA_PARAM[j]))
            hp_limiter_type_aura_per[j] = int(hp_limiter_type_aura_per[j] * _hp_4 * _hp_1 )

            _atk_3 = atk_base[hero_level_list[j]]
            atk_limiter_type_aura.append(int(_atk_3 * _atk_2 * LIMITER_PVE_TYPE_AURA_PARAM[j]))
            atk_limiter_type_aura_per[j] = int(atk_limiter_type_aura_per[j] * _atk_4 * _atk_1 )

            _def_3 = def_base[hero_level_list[j]]
            def_limiter_type_aura.append(int(_def_3 * _def_2 * LIMITER_PVE_TYPE_AURA_PARAM[j]))
            def_limiter_type_aura_per[j] = int(def_limiter_type_aura_per[j] * _def_4 * _def_1 )

        # 优化属性值
        for j in range(0, 10):
            hp_limiter_type_aura[j] = int((j + 1) / 10 * hp_limiter_type_aura[9] )
            atk_limiter_type_aura[j] = int((j + 1) / 10 * atk_limiter_type_aura[9] )
            def_limiter_type_aura[j] = int((j + 1) / 10 * def_limiter_type_aura[9] )

        hp_max_type_aura, atk_max_type_aura, def_max_type_aura = cal_property(_level_list_1, _quality_list_1,
                                                                              hp_limiter_type_aura_per[9] / 10000,
                                                                              atk_limiter_type_aura_per[9] / 10000,
                                                                              def_limiter_type_aura_per[9] / 10000,
                                                                              False)

    # 计算限制器PVP属性及光环
    # 1. 计算标准等级基础属性
    hero_level_list_pvp = [256, 258, 260, 262, 264, 266, 268, 272, 276, 280]
    hero_quality_list_pvp = [9, 10, 11, 12, 13, 14, 15, 16, 16, 16, 16, 16, 16]
    hp_base_pvp, atk_base_pvp, def_base_pvp = cal_property(hero_level_list_pvp, hero_quality_list_pvp)

    # 2. 计算限制器基础属性
    df_limiter = pd.read_excel('design/limiter_offset.xlsx', sheet_name='all', index_col=0, header=0)
    hp_limiter_pvp = []
    atk_limiter_pvp = []
    def_limiter_pvp = []
    hp_limiter_per_pvp = [35, 70, 105, 140, 175, 210, 245, 280, 315, 350]
    atk_limiter_per_pvp = [35, 70, 105, 140, 175, 210, 245, 280, 315, 350]
    def_limiter_per_pvp = [35, 70, 105, 140, 175, 210, 245, 280, 315, 350]
    _level_list_1_pvp = [280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280]
    _quality_list_1_pvp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    _hp_1 = df_limiter.loc[v, '_hp']
    _atk_1 = df_limiter.loc[v, '_atk']
    _def_1 = df_limiter.loc[v, '_def']

    for j in range(0, 10):
        _hp_3 = hp_base_pvp[hero_level_list_pvp[j]]
        hp_limiter_pvp.append(int(_hp_3 * _hp_1 * LIMITER_PVP_VALUE_PARAM[j] * _complete_param))
        hp_limiter_per_pvp[j] = int(hp_limiter_per_pvp[j] * _hp_1 * _complete_param)

        _atk_3 = atk_base_pvp[hero_level_list_pvp[j]]
        atk_limiter_pvp.append(int(_atk_3 * _atk_1 * LIMITER_PVP_VALUE_PARAM[j] * _complete_param))
        atk_limiter_per_pvp[j] = int(atk_limiter_per_pvp[j] * _atk_1 * _complete_param)

        _def_3 = def_base_pvp[hero_level_list_pvp[j]]
        def_limiter_pvp.append(int(_def_3 * _def_1 * LIMITER_PVP_VALUE_PARAM[j] * _complete_param))
        def_limiter_per_pvp[j] = int(def_limiter_per_pvp[j] * _def_1 * _complete_param)

    hp_max_pvp, atk_max_pvp, def_max_pvp = cal_property(_level_list_1_pvp, _quality_list_1_pvp,
                                                        hp_limiter_per_pvp[9] / 10000,
                                                        atk_limiter_per_pvp[9] / 10000,
                                                        def_limiter_per_pvp[9] / 10000, False)

    # 3. 计算限制器全体光环
    hp_limiter_aura_pvp = []
    atk_limiter_aura_pvp = []
    def_limiter_aura_pvp = []
    hp_limiter_aura_per_pvp = [35, 70, 105, 140, 175, 210, 245, 280, 315, 350]
    atk_limiter_aura_per_pvp = [35, 70, 105, 140, 175, 210, 245, 280, 315, 350]
    def_limiter_aura_per_pvp = [35, 70, 105, 140, 175, 210, 245, 280, 315, 350]

    _hp_4 = df_hero.loc[_id, '_aura_hp']
    _atk_4 = df_hero.loc[_id, '_aura_atk']
    _def_4 = df_hero.loc[_id, '_aura_def']
    _type = get_offset_type(_hp_4, _atk_4, _def_4)

    df_limiter = pd.read_excel('design/limiter_offset.xlsx', sheet_name=_type, index_col=0, header=0)
    _hp_2 = df_limiter.loc[v, '_hp']
    _atk_2 = df_limiter.loc[v, '_atk']
    _def_2 = df_limiter.loc[v, '_def']
    for j in range(0, 10):
        _hp_3 = hp_base_pvp[hero_level_list_pvp[j]]
        hp_limiter_aura_pvp.append(int(_hp_3 * _hp_2 * LIMITER_PVP_AURA_PARAM[j]))
        hp_limiter_aura_per_pvp[j] = int(hp_limiter_aura_per_pvp[j] * _hp_4 * _hp_1)

        _atk_3 = atk_base_pvp[hero_level_list_pvp[j]]
        atk_limiter_aura_pvp.append(int(_atk_3 * _atk_2 * LIMITER_PVP_AURA_PARAM[j]))
        atk_limiter_aura_per_pvp[j] = int(atk_limiter_aura_per_pvp[j] * _atk_4 * _atk_1)

        _def_3 = def_base_pvp[hero_level_list_pvp[j]]
        def_limiter_aura_pvp.append(int(_def_3 * _def_2 * LIMITER_PVP_AURA_PARAM[j]))
        def_limiter_aura_per_pvp[j] = int(def_limiter_aura_per_pvp[j] * _def_4 * _def_1)

    hp_max_aura_pvp, atk_max_aura_pvp, def_max_aura_pvp = cal_property(_level_list_1_pvp, _quality_list_1_pvp,
                                                                       hp_limiter_aura_per_pvp[9] / 10000,
                                                                       atk_limiter_aura_per_pvp[9] / 10000,
                                                                       def_limiter_aura_per_pvp[9] / 10000, False)

    # 3. 计算限制器阵营光环
    _hp_4 = df_hero.loc[_id, '_type_aura_hp']
    _atk_4 = df_hero.loc[_id, '_type_aura_atk']
    _def_4 = df_hero.loc[_id, '_type_aura_def']
    _type = get_offset_type(_hp_4, _atk_4, _def_4)

    if _type == 'none':
        hp_limiter_type_aura_pvp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        atk_limiter_type_aura_pvp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        def_limiter_type_aura_pvp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hp_limiter_type_aura_per_pvp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        atk_limiter_type_aura_per_pvp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        def_limiter_type_aura_per_pvp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hp_max_type_aura_pvp, atk_max_type_aura_pvp, def_max_type_aura_pvp = cal_property(_level_list_1_pvp,
                                                                                          _quality_list_1_pvp, 0, False)
    else:
        df_limiter = pd.read_excel('design/limiter_offset.xlsx', sheet_name=_type, index_col=0, header=0)
        hp_limiter_type_aura_pvp = []
        atk_limiter_type_aura_pvp = []
        def_limiter_type_aura_pvp = []
        hp_limiter_type_aura_per_pvp = [17, 35, 52, 70, 87, 105, 122, 140, 157, 175]
        atk_limiter_type_aura_per_pvp = [17, 35, 52, 70, 87, 105, 122, 140, 157, 175]
        def_limiter_type_aura_per_pvp = [17, 35, 52, 70, 87, 105, 122, 140, 157, 175]

        _hp_2 = df_limiter.loc[v, '_hp']
        _atk_2 = df_limiter.loc[v, '_atk']
        _def_2 = df_limiter.loc[v, '_def']
        for j in range(0, 10):
            _hp_3 = hp_base_pvp[hero_level_list_pvp[j]]
            hp_limiter_type_aura_pvp.append(int(_hp_3 * _hp_2 * LIMITER_PVP_TYPE_AURA_PARAM[j]))
            hp_limiter_type_aura_per_pvp[j] = int(hp_limiter_type_aura_per_pvp[j] * _hp_4 * _hp_1)

            _atk_3 = atk_base_pvp[hero_level_list_pvp[j]]
            atk_limiter_type_aura_pvp.append(int(_atk_3 * _atk_2 * LIMITER_PVP_TYPE_AURA_PARAM[j]))
            atk_limiter_type_aura_per_pvp[j] = int(atk_limiter_type_aura_per_pvp[j] * _atk_4 * _atk_1)

            _def_3 = def_base_pvp[hero_level_list_pvp[j]]
            def_limiter_type_aura_pvp.append(int(_def_3 * _def_2 * LIMITER_PVP_TYPE_AURA_PARAM[j]))
            def_limiter_type_aura_per_pvp[j] = int(def_limiter_type_aura_per_pvp[j] * _def_4 * _def_1)

    hp_max_type_aura_pvp, atk_max_type_aura_pvp, def_max_type_aura_pvp \
        = cal_property(_level_list_1_pvp, _quality_list_1_pvp, hp_limiter_type_aura_per_pvp[9] / 10000,
                       atk_limiter_type_aura_per_pvp[9] / 10000, def_limiter_type_aura_per_pvp[9] / 10000, False)

    sv.save_hero_limiter_growth(_id, hp_limiter, hp_limiter_per, hp_limiter_aura, hp_limiter_aura_per,
                                hp_limiter_type_aura, hp_limiter_type_aura_per, hp_limiter_pvp, hp_limiter_per_pvp,
                                hp_limiter_aura_pvp, hp_limiter_aura_per_pvp, hp_limiter_type_aura_pvp,
                                hp_limiter_type_aura_per_pvp, atk_limiter, atk_limiter_per, atk_limiter_aura,
                                atk_limiter_aura_per, atk_limiter_type_aura, atk_limiter_type_aura_per, atk_limiter_pvp,
                                atk_limiter_per_pvp, atk_limiter_aura_pvp, atk_limiter_aura_per_pvp,
                                atk_limiter_type_aura_pvp, atk_limiter_type_aura_per_pvp, def_limiter, def_limiter_per,
                                def_limiter_aura, def_limiter_aura_per, def_limiter_type_aura,
                                def_limiter_type_aura_per, def_limiter_pvp, def_limiter_per_pvp, def_limiter_aura_pvp,
                                def_limiter_aura_per_pvp, def_limiter_type_aura_pvp, def_limiter_type_aura_per_pvp)
    sv.save_hero_quality_max_value(_id, hp_max, atk_max, def_max, hp_max_pvp, atk_max_pvp, def_max_pvp, hp_max_aura,
                                   atk_max_aura, def_max_aura, hp_max_aura_pvp, atk_max_aura_pvp, def_max_aura_pvp,
                                   hp_max_type_aura, atk_max_type_aura, def_max_type_aura, hp_max_type_aura_pvp,
                                   atk_max_type_aura_pvp, def_max_type_aura_pvp)

    print('已经处理完 ' + _name)
