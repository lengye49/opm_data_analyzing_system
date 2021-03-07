import pandas as pd
import load_hero_info as ld
import save_hero_info as sv


def get_grade(level):
    if level <= 10:
        return 1
    else:
        return min(19, int((level - 1) / 20) + 2)


def get_real_level(level, enhance):
    if level < 240:
        return level
    else:
        return (level - 240) * 10 + 240 + enhance


def get_pvp_level(_l):
    return 240 + int(_l / 10)


hero_list = [1]
df_status = pd.read_excel('design/hero_design.xlsx', sheet_name='设定状态', index_col=0, header=0)
df_status.dropna(axis=0, how='all')
status_list = df_status.index.values

# 提前加载的信息
# 研究所机械核心
df_academy = pd.read_excel('design/academy.xlsx', index_col=0, header=0)
# 等级成长
df_level_growth = pd.read_excel('design/level_growth.xlsx', index_col=0, header=0)
# 装备信息
df_equip = pd.read_excel('design/equip_design.xlsx', index_col=0, header=0)

for _id in hero_list:
    # 加载基础信息
    hero_id, hero_name, hero_camp, hero_profession, hero_job, hp_init, atk_init, def_init, crit_init \
        = ld.load_hero_basic_info(_id)

    # 加载品质信息
    hp_per_quality, atk_per_quality, def_per_quality, hp_v_quality, atk_v_quality, def_v_quality, \
    hp_pve_max, atk_pve_max, def_pve_max, hp_pve_aura_max, atk_pve_aura_max, def_pve_aura_max, \
    hp_pve_type_aura_max, atk_pve_type_aura_max, def_pve_type_aura_max, \
    hp_pvp_max, atk_pvp_max, def_pvp_max, hp_pvp_aura_max, atk_pvp_aura_max, def_pvp_aura_max, \
    hp_pvp_type_aura_max, atk_pvp_type_aura_max, def_pvp_type_aura_max \
        = ld.load_hero_quality_growth(_id)

    # 加载品阶信息
    hp_v_grade, atk_v_grade, def_v_grade = ld.load_hero_grade_growth(_id)

    # 加载天赋信息
    talent_lv = 41 if hero_camp == 5 else 31
    hp_per_talent, atk_per_talent, def_per_talent, crit_talent, crit_res_talent, precise_talent, \
    parry_talent, dmg_res_talent \
        = ld.load_hero_talent(_id, talent_lv)

    # 加载机械核心信息
    hp_pve_mechanical, atk_pve_mechanical, def_pve_mechanical, \
    hp_pvp_mechanical, atk_pvp_mechanical, def_pvp_mechanical \
        = ld.load_hero_mechanical_power(_id)

    # 加载限制器信息
    hp_pve_v_limiter, hp_pve_per_limiter, hp_pve_aura_limiter, \
    hp_pve_aura_per_limiter, hp_pve_type_aura_limiter, hp_pve_type_aura_per_limiter, \
    hp_pvp_v_limiter, hp_pvp_per_limiter, hp_pvp_aura_limiter, \
    hp_pvp_aura_per_limiter, hp_pvp_type_aura_limiter, hp_pvp_type_aura_per_limiter, \
    atk_pve_v_limiter, atk_pve_per_limiter, atk_pve_aura_limiter, \
    atk_pve_aura_per_limiter, atk_pve_type_aura_limiter, atk_pve_type_aura_per_limiter, \
    atk_pvp_v_limiter, atk_pvp_per_limiter, atk_pvp_aura_limiter, \
    atk_pvp_aura_per_limiter, atk_pvp_type_aura_limiter, atk_pvp_type_aura_per_limiter, \
    def_pve_v_limiter, def_pve_per_limiter, def_pve_aura_limiter, \
    def_pve_aura_per_limiter, def_pve_type_aura_limiter, def_pve_type_aura_per_limiter, \
    def_pvp_v_limiter, def_pvp_per_limiter, def_pvp_aura_limiter, \
    def_pvp_aura_per_limiter, def_pvp_type_aura_limiter, def_pvp_type_aura_per_limiter \
        = ld.load_hero_limiter(_id)

    # 加载职阶信息
    df_job = pd.read_excel('design/job_' + str(hero_job) + '.xlsx', index_col=0)

    # 计算各个状态的属性
    final_hp = []
    final_atk = []
    final_def = []
    final_crit = []
    final_crit_res = []
    final_crit_dmg = []
    final_precise = []
    final_parry = []
    final_dmg_res = []
    for i in status_list:
        _type = df_status.loc[i, '_type']
        _quality = df_status.loc[i, '_quality']

        _level = df_status.loc[i, '_pve_level']
        _lv_enhance = df_status.loc[i, '_lv_enhance']
        if _type == 'pvp':
            _level = get_pvp_level(_level)
            _lv_enhance = 0
        _real_lv = get_real_level(_level, _lv_enhance)

        _e_qua = df_status.loc[i, '_e_qua']
        _e_enhance = df_status.loc[i, '_e_enhance']
        _talent = df_status.loc[i, '_talent']
        _core = df_status.loc[i, '_core']
        _job = df_status.loc[i, '_job']
        _limiter = df_status.loc[i, '_limiter']
        _mechanical = df_status.loc[i, '_mechanical']

        # 基础属性
        _hp_base = hp_init + df_level_growth.loc[
            _real_lv, '_hp_inc'] * hp_per_quality / 10000 + hp_v_quality + hp_v_grade
        _atk_base = atk_init + df_level_growth.loc[
            _real_lv, '_atk_inc'] * atk_per_quality / 10000 + atk_v_quality + atk_v_grade
        _def_base = def_init + df_level_growth.loc[
            _real_lv, '_def_inc'] * def_per_quality / 10000 + def_v_quality + def_v_grade

        # 装备属性
        _equip_1 = hero_profession * 1000 + 10 + 100
        _equip_2 = hero_profession * 1000 + 10 + 200
        _equip_3 = hero_profession * 1000 + 10 + 300
        _equip_4 = hero_profession * 1000 + 10 + 400
        _hp_equip = (df_equip.loc[_equip_1, '_hp'] + df_equip.loc[_equip_2, '_hp'] + df_equip.loc[_equip_3, '_hp'] +
                     df_equip.loc[_equip_4, '_hp']) * 1.5
        _atk_equip = (df_equip.loc[_equip_1, '_atk'] + df_equip.loc[_equip_2, '_atk'] + df_equip.loc[_equip_3, '_atk'] +
                      df_equip.loc[_equip_4, '_atk']) * 1.5
        _def_equip = (df_equip.loc[_equip_1, '_def'] + df_equip.loc[_equip_2, '_def'] + df_equip.loc[_equip_3, '_def'] +
                      df_equip.loc[_equip_4, '_def']) * 1.5
        _crit_equip = (df_equip.loc[_equip_1, '_crit'] + df_equip.loc[_equip_2, '_crit'] + df_equip.loc[
            _equip_3, '_crit'] +
                       df_equip.loc[_equip_4, '_crit']) / 10000 * 1.5
        _crit_res_equip = (df_equip.loc[_equip_1, '_crit_res'] + df_equip.loc[_equip_2, '_crit_res'] + df_equip.loc[
            _equip_3, '_crit_res'] + df_equip.loc[_equip_4, '_crit_res']) / 10000 * 1.5
        _precise_equip = (df_equip.loc[_equip_1, '_precise'] + df_equip.loc[_equip_2, '_precise'] + df_equip.loc[
            _equip_3, '_precise'] + df_equip.loc[_equip_4, '_precise']) / 10000 * 1.5
        _parry_equip = (df_equip.loc[_equip_1, '_parry'] + df_equip.loc[_equip_2, '_parry'] + df_equip.loc[
            _equip_3, '_parry'] + df_equip.loc[_equip_4, '_parry']) / 10000 * 1.5
        _dmg_res_equip = (df_equip.loc[_equip_1, '_dmg_res'] + df_equip.loc[_equip_2, '_dmg_res'] + df_equip.loc[
            _equip_3, '_dmg_res'] + df_equip.loc[_equip_4, '_dmg_res']) / 10000 * 1.5

        # 天赋属性
        _hp_talent = _hp_base * hp_per_talent[_talent] / 10000
        _atk_talent = _atk_base * atk_per_talent[_talent] / 10000
        _def_talent = _def_base * def_per_talent[_talent] / 10000
        _crit_talent = crit_talent[_talent]
        _crit_res_talent = crit_res_talent[_talent]
        _precise_talent = precise_talent[_talent]
        _parry_talent = parry_talent[_talent]
        _dmg_res_talent = dmg_res_talent[_talent]

        # 研究所核心属性
        _hp_academy = df_academy.loc[_core,'_hp_' + _type]
        _atk_academy = df_academy.loc[_core, '_atk_' + _type]
        _def_academy = df_academy.loc[_core, '_def_' + _type]

        # 职阶属性
        _hp_job = df_job.loc[_job, '_hp' + _type]
        _atk_job = df_job.loc[_job, '_atk' + _type]
        _def_job = df_job.loc[_job, '_def' + _type]
        _crit_job = df_job.loc[_job, '_crit' + _type]
        _crit_res_job = df_job.loc[_job, '_crit_res' + _type]
        _precise_job = df_job.loc[_job, '_precise' + _type]
        _parry_job = df_job.loc[_job, '_parry' + _type]
        _dmg_res_job = df_job.loc[_job, '_dmg_res' + _type]

        # 机械核心属性
        if _type == 'pve':
            _hp_mechanical = hp_pve_mechanical[_mechanical]
            _atk_mechanical = atk_pve_mechanical[_mechanical]
            _def_mechanical = def_pve_mechanical[_mechanical]
        else:
            _hp_mechanical = hp_pvp_mechanical[_mechanical]
            _atk_mechanical = atk_pvp_mechanical[_mechanical]
            _def_mechanical = def_pvp_mechanical[_mechanical]

        # 限制器属性 1为固定值 2为百分比 3为光环固定值 4为光环百分比 5为阵营光环固定值 6为阵营光环百分比
        #          12、14、16为百分比转固定值
        #          11、13、15为百分比+固定值
        if _type == 'pve':
            hp1 = hp_pve_v_limiter[_limiter]
            atk1 = atk_pve_v_limiter[_limiter]
            def1 = def_pve_v_limiter[_limiter]

            hp2 = hp_pve_per_limiter[_limiter]
            atk2 = atk_pve_per_limiter[_limiter]
            def2 = def_pve_per_limiter[_limiter]

            hp12 = min(_hp_base * hp2 / 10000, hp_pve_max)
            atk12 = min(_atk_base * atk2 / 10000, atk_pve_max)
            def12 = min(_def_base * def2 / 10000, def_pve_max)

            hp11 = hp1 + hp12
            atk11 = atk1 + atk12
            def11 = def1 + def12

            hp3 = hp_pve_aura_limiter[_limiter]
            atk3 = atk_pve_aura_limiter[_limiter]
            def3 = def_pve_aura_limiter[_limiter]

            hp4 = hp_pve_aura_per_limiter[_limiter]
            atk4 = atk_pve_aura_per_limiter[_limiter]
            def4 = def_pve_aura_per_limiter[_limiter]

            hp14 = min(_hp_base * hp4 / 10000, hp_pve_aura_max)
            atk14 = min(_atk_base * atk4 / 10000, atk_pve_aura_max)
            def14 = min(_def_base * def4 / 10000, def_pve_aura_max)

            hp13 = hp3 + hp14
            atk13 = atk3 + atk14
            def13 = def3 + def14

            hp5 = hp_pve_type_aura_limiter[_limiter]
            atk5 = atk_pve_type_aura_limiter[_limiter]
            def5 = def_pve_type_aura_limiter[_limiter]

            hp6 = hp_pve_type_aura_per_limiter[_limiter]
            atk6 = atk_pve_type_aura_per_limiter[_limiter]
            def6 = def_pve_type_aura_per_limiter[_limiter]

            hp16 = min(_hp_base * hp6 / 10000, hp_pve_type_aura_max)
            atk16 = min(_atk_base * atk6 / 10000, atk_pve_type_aura_max)
            def16 = min(_def_base * def6 / 10000, def_pve_type_aura_max)

            hp15 = hp5 + hp16
            atk15 = atk5 + atk16
            def15 = def5 + def16
        else:
            hp1 = hp_pvp_v_limiter[_limiter]
            atk1 = atk_pvp_v_limiter[_limiter]
            def1 = def_pvp_v_limiter[_limiter]

            hp2 = hp_pvp_per_limiter[_limiter]
            atk2 = atk_pvp_per_limiter[_limiter]
            def2 = def_pvp_per_limiter[_limiter]

            hp12 = min(_hp_base * hp2 / 10000, hp_pvp_max)
            atk12 = min(_atk_base * atk2 / 10000, atk_pvp_max)
            def12 = min(_def_base * def2 / 10000, def_pvp_max)

            hp11 = hp1 + hp12
            atk11 = atk1 + atk12
            def11 = def1 + def12

            hp3 = hp_pvp_aura_limiter[_limiter]
            atk3 = atk_pvp_aura_limiter[_limiter]
            def3 = def_pvp_aura_limiter[_limiter]

            hp4 = hp_pvp_aura_per_limiter[_limiter]
            atk4 = atk_pvp_aura_per_limiter[_limiter]
            def4 = def_pvp_aura_per_limiter[_limiter]

            hp14 = min(_hp_base * hp4 / 10000, hp_pvp_aura_max)
            atk14 = min(_atk_base * atk4 / 10000, atk_pvp_aura_max)
            def14 = min(_def_base * def4 / 10000, def_pvp_aura_max)

            hp13 = hp3 + hp14
            atk13 = atk3 + atk14
            def13 = def3 + def14

            hp5 = hp_pvp_type_aura_limiter[_limiter]
            atk5 = atk_pvp_type_aura_limiter[_limiter]
            def5 = def_pvp_type_aura_limiter[_limiter]

            hp6 = hp_pvp_type_aura_per_limiter[_limiter]
            atk6 = atk_pvp_type_aura_per_limiter[_limiter]
            def6 = def_pvp_type_aura_per_limiter[_limiter]

            hp16 = min(_hp_base * hp6 / 10000, hp_pvp_type_aura_max)
            atk16 = min(_atk_base * atk6 / 10000, atk_pvp_type_aura_max)
            def16 = min(_def_base * def6 / 10000, def_pvp_type_aura_max)

            hp15 = hp5 + hp16
            atk15 = atk5 + atk16
            def15 = def5 + def16

        _hp_limiter = hp11
        _hp_limiter_aura = hp13
        _hp_limiter_type_aura = hp15

        _atk_limiter = atk11
        _atk_limiter_aura = atk13
        _atk_limiter_type_aura = atk15

        _def_limiter = def11
        _def_limiter_aura = def13
        _def_limiter_type_aura = def15

        _hp = _hp_base + _hp_equip + _hp_talent + _hp_academy + _hp_job + _hp_mechanical + _hp_limiter
        _atk = _atk_base + _atk_equip + _atk_talent + _atk_academy + _atk_job + _atk_mechanical + _atk_limiter
        _def = _def_base + _def_equip + _def_talent + _def_academy + _def_job + _def_mechanical + _def_limiter
        _crit = crit_init + _crit_equip + _crit_talent + _crit_job
        _crit_res = _crit_res_equip + _crit_res_talent + _crit_res_job
        _crit_dmg = 15000
        _precise = _precise_equip + _precise_talent + _precise_job
        _parry = _parry_equip + _parry_talent + _parry_job
        _dmg_res = _dmg_res_equip + _dmg_res_talent + _dmg_res_job

        final_hp.append(_hp)
        final_atk.append(_atk)
        final_def.append(_def)
        final_crit.append(_crit)
        final_crit_res.append(_crit_res)
        final_crit_dmg.append(_crit_dmg)
        final_precise.append(_precise)
        final_parry.append(_parry)
        final_dmg_res.append(_dmg_res)


print(_id)
