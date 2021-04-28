import pandas as pd
import save_hero_info as sv
import opm_property_tools as tools

hero_list = [109]

# 属性总值
HP_STD = 304808
ATK_STD = 50000
DEF_STD = 36290
CRIT_STD = 0.239144068
CRIT_RES_STD = 0.125147458
CRIT_DMG_STD = 20000
PRECISE_STD = 0.1287
PARRY_STD = 0.299615254
DMG_RES_STD = 0.21109322

# 品阶占240级属性比例
GRADE_PERCENT = 0.1

# 初始属性占240级属性比例
INIT_HP_PERCENT = 0.004 * 4 / 7
INIT_ATK_PERCENT = 0.004
INIT_DEF_PERCENT = 0.0016

# 品质属性占240级属性比例
HP_QUALITY_VALUE_PERCENT = 0.024 + 0.004 - INIT_HP_PERCENT
ATK_QUALITY_VALUE_PERCENT = 0.024
DEF_QUALITY_VALUE_PERCENT = 0.028

# 基础暴击
CRIT_BASE = 0.05

# 初始版本设定缘分属性
HP_PER_PARTNER = 0.08
ATK_PER_PARTNER = 0.1
DEF_PER_PARTNER = 0.1
HP_PARTNER = 4400
HP_PARTNER = 4400
ATK_PARTNER = 960
DEF_PARTNER = 400
CRIT_PARTNER = 0.05
CRIT_RES_PARTNER = 0.05
PRECISE_PARTNER = 0.05
PARRY_PARTNER = 0.05
DMG_RES_PARTNER = 0.05

# 240级等级成长属性
hp_inc_240 = 57822
atk_inc_240 = 10960
def_inc_240 = 3107

# 品质成长参数
HP_QUALITY_PER_PARAM = [0, 0, 0.0857142857142857, 0.182857142857143, 0.297142857142857, 0.482142857142857,
                        0.721428571428571, 1.02928571428571, 1.26, 1.54142857142857, 2.06, 2.14, 2.22, 2.3, 2.38, 2.46]
ATK_QUALITY_PER_PARAM = [0, 0, 0.15, 0.32, 0.52, 0.75, 1.01, 1.31, 1.47, 1.66, 2.06, 2.14, 2.22, 2.3, 2.38, 2.46]
DEF_QUALITY_PER_PARAM = [0, 0, 0.06, 0.128, 0.208, 0.375, 0.606, 0.917, 1.176, 1.494, 2.06, 2.14, 2.22, 2.3, 2.38, 2.46]
HP_QUALITY_VALUE_PARAM = [0, 0.024065892413428, 0.0481317848268559, 0.0721976772402839, 0.0989027958550511,
                          0.185439733991669, 0.274722189354452, 0.362639908068291, 0.428565412098325, 0.499996991763448,
                          0.615374896466525, 0.692305532548117, 0.769222130192467, 0.846152766274058, 0.923069363918409,
                          1]
ATK_QUALITY_VALUE_PARAM = [0, 0.0421153117234989, 0.0842306234469979, 0.126345935170497, 0.173079892746339,
                           0.288461808431485, 0.384611065096233, 0.461541701177825, 0.499992980781379,
                           0.538458298822175, 0.615374896466525, 0.692305532548117, 0.769222130192467,
                           0.846152766274058,
                           0.923069363918409, 1]
DEF_QUALITY_VALUE_PARAM = [0, 0.0168461246893996, 0.0336922493787991, 0.0505383740681987, 0.0692319570985358,
                           0.144230904215743, 0.23076663905774, 0.323079190824477, 0.399994384625104, 0.484612468939958,
                           0.615374896466525, 0.692305532548117, 0.769222130192467, 0.846152766274058,
                           0.923069363918409, 1]

# 品阶成长参数
HP_GRADE_VALUE_PARAM = [0.00714285714285714, 0.00928571428571429, 0.015, 0.0260714285714286, 0.0426666666666667,
                        0.0675952380952381, 0.107142857142857, 0.158333333333333, 0.238095238095238, 0.355, 0.5, 0.72,
                        1, 1, 1, 1, 1, 1, 1, 1]
ATK_GRADE_VALUE_PARAM = [0.0125, 0.015, 0.0225, 0.0365, 0.056, 0.0835, 0.125, 0.175, 0.25, 0.355, 0.5, 0.72, 1, 1, 1, 1,
                         1, 1, 1, 1]
DEF_GRADE_VALUE_PARAM = [0.005, 0.00675, 0.01125, 0.020075, 0.0336, 0.054275, 0.0875, 0.13125, 0.2, 0.30175, 0.45,
                         0.684, 1, 1, 1, 1, 1, 1, 1, 1]

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
df_equip = pd.read_excel('design/equip_design.xlsx', index_col=0, header=0)
df_level_growth = pd.read_excel('design/level_growth.xlsx', index_col=0, header=0)


# df_academy = pd.read_excel('design/academy.xlsx', index_col=0, header=0)


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
    _id = i
    _name = df_hero.loc[_id, '_name']
    _camp = df_hero.loc[_id, '_camp']
    _profession = df_hero.loc[_id, '_profession']
    _job = df_hero.loc[_id, '_job']
    # df_job = pd.read_excel('design/job_' + str(_job) + '.xlsx', index_col=0)
    _talent_lv = 41 if _camp == 5 else 31

    # 角色满级装备属性
    _equip_1 = _profession * 1000 + 10 + 100
    _equip_2 = _profession * 1000 + 10 + 200
    _equip_3 = _profession * 1000 + 10 + 300
    _equip_4 = _profession * 1000 + 10 + 400
    _hp_equip = (df_equip.loc[_equip_1, '_hp'] + df_equip.loc[_equip_2, '_hp'] + df_equip.loc[_equip_3, '_hp'] +
                 df_equip.loc[_equip_4, '_hp']) * 1.5
    _atk_equip = (df_equip.loc[_equip_1, '_atk'] + df_equip.loc[_equip_2, '_atk'] + df_equip.loc[_equip_3, '_atk'] +
                  df_equip.loc[_equip_4, '_atk']) * 1.5
    _def_equip = (df_equip.loc[_equip_1, '_def'] + df_equip.loc[_equip_2, '_def'] + df_equip.loc[_equip_3, '_def'] +
                  df_equip.loc[_equip_4, '_def']) * 1.5
    _crit_equip = (df_equip.loc[_equip_1, '_crit'] + df_equip.loc[_equip_2, '_crit'] + df_equip.loc[_equip_3, '_crit'] +
                   df_equip.loc[_equip_4, '_crit']) / 10000 * 1.5
    _crit_res_equip = (df_equip.loc[_equip_1, '_crit_res'] + df_equip.loc[_equip_2, '_crit_res'] + df_equip.loc[
        _equip_3, '_crit_res'] + df_equip.loc[_equip_4, '_crit_res']) / 10000 * 1.5
    _precise_equip = (df_equip.loc[_equip_1, '_precise'] + df_equip.loc[_equip_2, '_precise'] + df_equip.loc[
        _equip_3, '_precise'] + df_equip.loc[_equip_4, '_precise']) / 10000 * 1.5
    _parry_equip = (df_equip.loc[_equip_1, '_parry'] + df_equip.loc[_equip_2, '_parry'] + df_equip.loc[
        _equip_3, '_parry'] + df_equip.loc[_equip_4, '_parry']) / 10000 * 1.5
    _dmg_res_equip = (df_equip.loc[_equip_1, '_dmg_res'] + df_equip.loc[_equip_2, '_dmg_res'] + df_equip.loc[
        _equip_3, '_dmg_res'] + df_equip.loc[_equip_4, '_dmg_res']) / 10000 * 1.5

    # 角色天赋设定
    _hp_per_talent = (df_hero.loc[_id, '_talent_hp'] * _talent_lv) / 100
    _atk_per_talent = (df_hero.loc[_id, '_talent_atk'] * _talent_lv) / 100
    _def_per_talent = (df_hero.loc[_id, '_talent_def'] * _talent_lv) / 100
    _crit_talent = df_hero.loc[_id, '_talent_crit'] * _talent_lv
    _crit_res_talent = df_hero.loc[_id, '_talent_crit_res'] * _talent_lv
    _precise_talent = df_hero.loc[_id, '_talent_precise'] * _talent_lv
    _parry_talent = df_hero.loc[_id, '_talent_parry'] * _talent_lv
    _dmg_res_talent = df_hero.loc[_id, '_talent_dmg_res'] * _talent_lv

    # 角色属性偏移
    _hp_offset = df_hero.loc[_id, '_hp_offset']
    _atk_offset = df_hero.loc[_id, '_atk_offset']

    # 计算总生命、总攻击、总防御
    hp_total = HP_STD * _hp_offset
    atk_total = ATK_STD * _atk_offset

    crit_1 = _crit_talent + _crit_equip + CRIT_PARTNER + CRIT_BASE
    crit_res_1 = _crit_res_talent + _crit_res_equip + CRIT_RES_PARTNER
    precise_1 = _precise_talent + _precise_equip + PRECISE_PARTNER
    parry_1 = _parry_talent + _parry_equip + PARRY_PARTNER
    dmg_res_1 = _dmg_res_talent + _dmg_res_equip + DMG_RES_PARTNER

    _e_hp_std = HP_STD * (1 + DEF_STD / atk_total) / (1 - 0.5 * max(PARRY_STD - precise_1, 0)) / (1 - DMG_RES_STD)
    _e_atk_std = ATK_STD * max(1, 1 + CRIT_STD - crit_res_1)
    _e_atk1 = atk_total * max(1, 1 + crit_1 - CRIT_RES_STD)
    _e_hp1 = _e_hp_std * _e_atk_std / _e_atk1
    def_total = (_e_hp1 / hp_total * (1 - dmg_res_1) * (1 - 0.5 * max(parry_1 - PRECISE_STD, 0)) - 1) * ATK_STD

    # 计算240级基础属性
    hp_per_2 = _hp_per_talent + HP_PER_PARTNER
    atk_per_2 = _atk_per_talent + ATK_PER_PARTNER
    def_per_2 = _def_per_talent + DEF_PER_PARTNER
    hp_2 = _hp_equip + HP_PARTNER
    atk_2 = _atk_equip + ATK_PARTNER
    def_2 = _def_equip + DEF_PARTNER

    hp_240_1 = (hp_total - hp_2) / (1 + hp_per_2)
    atk_240_1 = (atk_total - atk_2) / (1 + atk_per_2)
    def_240_1 = (def_total - def_2) / (1 + def_per_2)

    # 计算突破总属性
    hp_grade = hp_240_1 * GRADE_PERCENT
    atk_grade = atk_240_1 * GRADE_PERCENT
    def_grade = def_240_1 * GRADE_PERCENT

    # 计算品质增加总值
    hp_quality = hp_240_1 * HP_QUALITY_VALUE_PERCENT
    atk_quality = atk_240_1 * ATK_QUALITY_VALUE_PERCENT
    def_quality = def_240_1 * DEF_QUALITY_VALUE_PERCENT

    # 计算初始属性
    hp_init = round(hp_240_1 * INIT_HP_PERCENT)
    atk_init = round(atk_240_1 * INIT_ATK_PERCENT)
    def_init = round(def_240_1 * INIT_DEF_PERCENT)

    # 计算等级属性
    hp_lv = hp_240_1 - hp_grade - hp_quality - hp_240_1 * INIT_HP_PERCENT
    atk_lv = atk_240_1 - atk_grade - atk_quality - atk_240_1 * INIT_ATK_PERCENT
    def_lv = def_240_1 - def_grade - def_quality - def_240_1 * INIT_DEF_PERCENT

    # 计算品质成长
    hp_quality_per = []
    atk_quality_per = []
    def_quality_per = []
    hp_quality_value = []
    atk_quality_value = []
    def_quality_value = []
    for j in range(0, 16):
        hp_quality_per.append(
            round((hp_lv / hp_inc_240 - 1) / HP_QUALITY_PER_PARAM[15] * HP_QUALITY_PER_PARAM[j] * 10000 + 10000))
        atk_quality_per.append(
            round((atk_lv / atk_inc_240 - 1) / ATK_QUALITY_PER_PARAM[15] * ATK_QUALITY_PER_PARAM[j] * 10000 + 10000))
        def_quality_per.append(
            round((def_lv / def_inc_240 - 1) / DEF_QUALITY_PER_PARAM[15] * DEF_QUALITY_PER_PARAM[j] * 10000 + 10000))

        hp_quality_value.append(round(hp_quality * HP_QUALITY_VALUE_PARAM[j]))
        atk_quality_value.append(round(atk_quality * ATK_QUALITY_VALUE_PARAM[j]))
        def_quality_value.append(round(def_quality * DEF_QUALITY_VALUE_PARAM[j]))

    # 计算品阶成长
    hp_grade_value = []
    atk_grade_value = []
    def_grade_value = []
    for j in range(0, 20):
        hp_grade_value.append(round(hp_grade * HP_GRADE_VALUE_PARAM[j]))
        atk_grade_value.append(round(atk_grade * ATK_GRADE_VALUE_PARAM[j]))
        def_grade_value.append(round(def_grade * DEF_GRADE_VALUE_PARAM[j]))

    # 计算角色天赋属性
    hp_talent_per = []
    atk_talent_per = []
    def_talent_per = []
    crit_talent_value = []
    crit_res_talent_value = []
    precise_talent_value = []
    parry_talent_value = []
    dmg_res_talent_value = []

    for j in range(0, _talent_lv):
        hp_talent_per.append(df_hero.loc[_id, '_talent_hp'] * (j + 1))
        atk_talent_per.append(df_hero.loc[_id, '_talent_atk'] * (j + 1))
        def_talent_per.append(df_hero.loc[_id, '_talent_def'] * (j + 1))
        crit_talent_value.append(df_hero.loc[_id, '_talent_crit'] * int((j + 5) / 10) * 10 * 10000)
        crit_res_talent_value.append(df_hero.loc[_id, '_talent_crit_res'] * int((j + 5) / 10) * 10 * 10000)
        precise_talent_value.append(df_hero.loc[_id, '_talent_precise'] * int((j + 5) / 10) * 10 * 10000)
        parry_talent_value.append(df_hero.loc[_id, '_talent_parry'] * int((j + 5) / 10) * 10 * 10000)
        dmg_res_talent_value.append(df_hero.loc[_id, '_talent_dmg_res'] * int((j + 5) / 10) * 10 * 10000)

    sv.save_hero_basic_info(_id, _name, _camp, _profession, _job, hp_init, atk_init, def_init)
    sv.save_hero_quality_growth(_id, hp_quality_per, atk_quality_per, def_quality_per, hp_quality_value,
                                atk_quality_value, def_quality_value)
    sv.save_hero_grade_growth(_id, hp_grade_value, atk_grade_value, def_grade_value)
    sv.save_hero_talent_growth(_id, _talent_lv, hp_talent_per, atk_talent_per, def_talent_per, crit_talent_value,
                               crit_res_talent_value, precise_talent_value, parry_talent_value, dmg_res_talent_value)

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

    # hp_base_pvp = {256: 250183.081632653, 258: 259467.367346939, 260: 269133.102040816, 262: 285515.897959184,
    #                264: 296227.693877551, 266: 307373.163265306, 268: 318972.551020408, 272: 343608.244897959,
    #                276: 370287.979591837, 280: 399185.326530612}
    # atk_base_pvp = {256: 43701.8979591837, 258: 45323.9795918367, 260: 47011.1020408163, 262: 49820.6326530612,
    #                 264: 51688.9387755102, 266: 53634.3673469388, 268: 55657.0816326531, 272: 59955.2448979592,
    #                 276: 64610.0408163265, 280: 69653.4285714286}
    # def_base_pvp = {256: 36370.5102040816, 258: 38052.8775510204, 260: 39805.4285714286, 262: 42869,
    #                 264: 44827.4285714286,
    #                 266: 46865.387755102, 268: 48982.7755102041, 272: 53484.8979591837, 276: 58355.7755102041,
    #                 280: 63631.2653061224}

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

    # 计算机械核心属性
    hp_400 = hp_base[400]
    atk_400 = atk_base[400]
    def_400 = def_base[400]

    hp_280 = hp_base_pvp[280]
    atk_280 = atk_base_pvp[280]
    def_280 = def_base_pvp[280]

    hp_mechanical_pve = []
    atk_mechanical_pve = []
    def_mechanical_pve = []

    hp_mechanical_pvp = []
    atk_mechanical_pvp = []
    def_mechanical_pvp = []

    for j in range(0, 30):
        v_pve = pow((j + 1) / 30, 2.1) * 1600
        hp_mechanical_pve.append(int(v_pve * hp_400 / 10000))
        atk_mechanical_pve.append(int(v_pve * atk_400 / 10000))
        def_mechanical_pve.append(int(v_pve * def_400 / 10000))

        # v_pvp = 1722 / 30 * (j + 1)
        v_pvp = v_pve  # 临时处理
        hp_mechanical_pvp.append(int(v_pvp * hp_280 / 10000))
        atk_mechanical_pvp.append(int(v_pvp * atk_280 / 10000))
        def_mechanical_pvp.append(int(v_pvp * def_280 / 10000))

    sv.save_hero_mechanical_power(_id, hp_mechanical_pve, atk_mechanical_pve, def_mechanical_pve,
                                  hp_mechanical_pvp, atk_mechanical_pvp, def_mechanical_pvp)
    print(i)
