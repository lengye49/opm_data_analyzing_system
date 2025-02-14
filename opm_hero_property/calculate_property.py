"""
这个脚本用于计算指定hero_list的角色属性，并将得到的属性以Bot表的格式存储到对应英雄数据的status页中
数据来源是 hero_design表里的hero_status页

其中装备类型加成采用了特殊设定（类型为10且强化等级>0才有加成）
"""

import pandas as pd
import load_hero_info as ld
import save_hero_info as sv
import opm_property_tools as tools

# 英雄列表
# hero_list = [1, 2, 8, 10, 11, 12, 13, 18, 19, 20, 21, 23, 24, 25, 26, 27, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42,
#              43, 44, 45, 46, 49, 51, 60, 61, 62, 63, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 100,
#              101, 102, 103, 104, 105, 107, 108, 109, 110, 111, 112, 114, 115]

hero_list = [12, 25, 60, 89, 116, 117, 118]

# 读取设定表
df_status = pd.read_excel('design/hero_design.xlsx', sheet_name='设定状态', index_col=0, header=0)
df_status.dropna(axis=0, how='all')
status_list = df_status.index.values
df_hero_info = pd.read_excel('design/hero_design.xlsx', sheet_name='卡牌设定', index_col=0, header=0)

# 提前读取通用配置
# 研究所机械核心
df_academy = pd.read_excel('design/academy.xlsx', index_col=0, header=0)
# 等级成长
df_level_growth = pd.read_excel('design/level_growth.xlsx', index_col=0, header=0)
# 装备信息
df_equip = pd.read_excel('design/equip_design.xlsx', index_col=0, header=0)
# 收集卡牌信息
df_collection_upgrade = pd.read_excel('design/collection_design.xlsx', sheet_name='upgrade', index_col=0, header=0)
df_collection_break = pd.read_excel('design/collection_design.xlsx', sheet_name='break', index_col=0, header=0)
df_collection_collect = pd.read_excel('design/collection_design.xlsx', sheet_name='collect', index_col=0, header=0)
# 正式数据处理
for _id in hero_list:

    # 加载基础信息
    hero_id, hero_name, hero_camp, hero_profession, hero_job, hp_init, atk_init, def_init, crit_init \
        = ld.load_hero_basic_info(_id)
    print('正在处理角色: ' + str(_id) + ' ' + hero_name)

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

    # 计算属性
    final_hp = []
    final_atk = []
    final_def = []
    final_crit = []
    final_crit_res = []
    final_crit_dmg = []
    final_precise = []
    final_parry = []
    final_dmg_res = []
    final_aura = []
    final_type_aura = []

    power_base = []
    power_equip = []
    power_talent = []
    power_academy = []
    power_job = []
    power_mechanical = []
    power_limiter = []
    power_collection = []
    power_total = []

    job_contact = []
    pvp_addition = []

    _level_list = []

    # 遍历各个状态
    for i in status_list:
        _type = df_status.loc[i, '_type']

        # 品质-1作为参数使用
        _quality = df_status.loc[i, '_quality'] - 1

        _level = df_status.loc[i, '_pve_level']
        _lv_enhance = df_status.loc[i, '_lv_enhance']
        if _type == 'pvp':
            _level = tools.get_pvp_level(_level)
            _lv_enhance = 0
        _real_lv = tools.get_real_level(_level, _lv_enhance)

        # 品阶-1作为参数使用
        _grade = tools.get_grade(_level) - 1

        _e_qua = df_status.loc[i, '_e_qua']
        _e_enhance = df_status.loc[i, '_e_enhance']
        _talent = df_status.loc[i, '_talent']
        _core = df_status.loc[i, '_core']
        _job = df_status.loc[i, '_job']
        _limiter = df_status.loc[i, '_limiter']
        _mechanical = df_status.loc[i, '_mechanical']
        _collection_upgrade = df_status.loc[i, '_collection_upgrade']
        _collection_break = df_status.loc[i, '_collection_break']
        _collection_collect = df_status.loc[i, '_collection_collect']

        # 基础属性
        _hp_base = hp_init + df_level_growth.loc[
            _real_lv, '_hp_inc'] * hp_per_quality[_quality] / 10000 + hp_v_quality[_quality] + hp_v_grade[_grade]
        _atk_base = atk_init + df_level_growth.loc[
            _real_lv, '_atk_inc'] * atk_per_quality[_quality] / 10000 + atk_v_quality[_quality] + atk_v_grade[_grade]
        _def_base = def_init + df_level_growth.loc[
            _real_lv, '_def_inc'] * def_per_quality[_quality] / 10000 + def_v_quality[_quality] + def_v_grade[_grade]
        _power_base = tools.get_power(_hp_base, _atk_base, _def_base, crit_init)

        # 装备属性
        _equip_1 = hero_profession * 1000 + _e_qua + 100
        _equip_2 = hero_profession * 1000 + _e_qua + 200
        _equip_3 = hero_profession * 1000 + _e_qua + 300
        _equip_4 = hero_profession * 1000 + _e_qua + 400

        if (_e_enhance > 0) and (_e_qua == 10):
            _adder = 1.0 + _e_enhance / 10.0 + 0.3
        elif _e_enhance > 0:
            _adder = 1.0 + _e_enhance / 10.0
        else:
            _adder = 1.0
        _hp_equip = (df_equip.loc[_equip_1, '_hp'] + df_equip.loc[_equip_2, '_hp'] + df_equip.loc[_equip_3, '_hp'] +
                     df_equip.loc[_equip_4, '_hp']) * _adder
        _atk_equip = (df_equip.loc[_equip_1, '_atk'] + df_equip.loc[_equip_2, '_atk'] + df_equip.loc[_equip_3, '_atk'] +
                      df_equip.loc[_equip_4, '_atk']) * _adder
        _def_equip = (df_equip.loc[_equip_1, '_def'] + df_equip.loc[_equip_2, '_def'] + df_equip.loc[_equip_3, '_def'] +
                      df_equip.loc[_equip_4, '_def']) * _adder
        _crit_equip = (df_equip.loc[_equip_1, '_crit'] + df_equip.loc[_equip_2, '_crit'] + df_equip.loc[
            _equip_3, '_crit'] + df_equip.loc[_equip_4, '_crit']) * _adder
        _crit_res_equip = (df_equip.loc[_equip_1, '_crit_res'] + df_equip.loc[_equip_2, '_crit_res'] + df_equip.loc[
            _equip_3, '_crit_res'] + df_equip.loc[_equip_4, '_crit_res']) * _adder
        _precise_equip = (df_equip.loc[_equip_1, '_precise'] + df_equip.loc[_equip_2, '_precise'] + df_equip.loc[
            _equip_3, '_precise'] + df_equip.loc[_equip_4, '_precise']) * _adder
        _parry_equip = (df_equip.loc[_equip_1, '_parry'] + df_equip.loc[_equip_2, '_parry'] + df_equip.loc[
            _equip_3, '_parry'] + df_equip.loc[_equip_4, '_parry']) * _adder
        _dmg_res_equip = (df_equip.loc[_equip_1, '_dmg_res'] + df_equip.loc[_equip_2, '_dmg_res'] + df_equip.loc[
            _equip_3, '_dmg_res'] + df_equip.loc[_equip_4, '_dmg_res']) * _adder

        _power_equip = tools.get_power(_hp_equip, _atk_equip, _def_equip, _crit_equip, _crit_res_equip, _precise_equip,
                                       _parry_equip, _dmg_res_equip)

        # 天赋属性
        if _talent >= 0:
            _hp_talent = _hp_base * hp_per_talent[_talent] / 10000
            _atk_talent = _atk_base * atk_per_talent[_talent] / 10000
            _def_talent = _def_base * def_per_talent[_talent] / 10000
            _crit_talent = crit_talent[_talent]
            _crit_res_talent = crit_res_talent[_talent]
            _precise_talent = precise_talent[_talent]
            _parry_talent = parry_talent[_talent]
            _dmg_res_talent = dmg_res_talent[_talent]

        else:
            _hp_talent = 0
            _atk_talent = 0
            _def_talent = 0
            _crit_talent = 0
            _crit_res_talent = 0
            _precise_talent = 0
            _parry_talent = 0
            _dmg_res_talent = 0

        _power_talent = tools.get_power(_hp_talent, _atk_talent, _def_talent, _crit_talent, _crit_res_talent,
                                        _precise_talent, _parry_talent, _dmg_res_talent)
        # 研究所核心属性
        if _core == 0:
            _hp_academy = 0
            _atk_academy = 0
            _def_academy = 0
        else:
            _hp_academy = df_academy.loc[_core, '_hp_' + _type]
            _atk_academy = df_academy.loc[_core, '_atk_' + _type]
            _def_academy = df_academy.loc[_core, '_def_' + _type]

        _power_academy = tools.get_power(_hp_academy, _atk_academy, _def_academy)

        # 职阶属性
        _job_contact = 0
        if _job == 0:
            _hp_job = 0
            _atk_job = 0
            _def_job = 0
            _crit_job = 0
            _crit_res_job = 0
            _precise_job = 0
            _parry_job = 0
            _dmg_res_job = 0
        else:
            # 增加职阶连携
            _hp_job = df_job.loc[_job, '_hp_' + _type] + int(_job / 10) * 0.01 * _hp_base
            _atk_job = df_job.loc[_job, '_atk_' + _type] + int(_job / 10) * 0.01 * _atk_base
            _def_job = df_job.loc[_job, '_def_' + _type] + int(_job / 10) * 0.01 * _def_base
            _crit_job = df_job.loc[_job, '_crit_' + _type]
            _crit_res_job = df_job.loc[_job, '_crit_res_' + _type]
            _precise_job = df_job.loc[_job, '_precise_' + _type]
            _parry_job = df_job.loc[_job, '_parry_' + _type]
            _dmg_res_job = df_job.loc[_job, '_dmg_res_' + _type]

            _job_contact = int(_job / 10) * 10

        _power_job = tools.get_power(_hp_job, _atk_job, _def_job, _crit_job, _crit_res_job, _precise_job, _parry_job,
                                     _dmg_res_job)

        # 机械核心属性
        if _mechanical > 0:

            # 机械核心等级-1作为参数使用
            _mechanical -= 1

            if _type == 'pve':
                _hp_mechanical = hp_pve_mechanical[_mechanical]
                _atk_mechanical = atk_pve_mechanical[_mechanical]
                _def_mechanical = def_pve_mechanical[_mechanical]
            else:
                _hp_mechanical = hp_pvp_mechanical[_mechanical]
                _atk_mechanical = atk_pvp_mechanical[_mechanical]
                _def_mechanical = def_pvp_mechanical[_mechanical]
        else:
            _hp_mechanical = 0
            _atk_mechanical = 0
            _def_mechanical = 0

        _power_mechanical = tools.get_power(_hp_mechanical, _atk_mechanical, _def_mechanical)

        # 限制器属性 1为固定值 2为百分比 3为光环固定值 4为光环百分比 5为阵营光环固定值 6为阵营光环百分比
        #          12、14、16为百分比转固定值
        #          11、13、15为百分比+固定值
        _limiter_on = (df_hero_info.loc[_id, '_limiter_on'] == 1)
        if _limiter_on and _limiter > 0:

            # 限制器等级-1作为参数使用
            _limiter -= 1

            if _type == 'pve':
                hp1 = hp_pve_v_limiter[_limiter]
                atk1 = atk_pve_v_limiter[_limiter]
                def1 = def_pve_v_limiter[_limiter]

                hp2 = hp_pve_per_limiter[_limiter]
                atk2 = atk_pve_per_limiter[_limiter]
                def2 = def_pve_per_limiter[_limiter]

                hp12 = min(_hp_base * hp2 / 10000, hp_pve_max[_quality])
                atk12 = min(_atk_base * atk2 / 10000, atk_pve_max[_quality])
                def12 = min(_def_base * def2 / 10000, def_pve_max[_quality])

                hp11 = hp1 + hp12
                atk11 = atk1 + atk12
                def11 = def1 + def12

                hp3 = hp_pve_aura_limiter[_limiter]
                atk3 = atk_pve_aura_limiter[_limiter]
                def3 = def_pve_aura_limiter[_limiter]

                hp4 = hp_pve_aura_per_limiter[_limiter]
                atk4 = atk_pve_aura_per_limiter[_limiter]
                def4 = def_pve_aura_per_limiter[_limiter]

                hp14 = min(_hp_base * hp4 / 10000, hp_pve_aura_max[_quality])
                atk14 = min(_atk_base * atk4 / 10000, atk_pve_aura_max[_quality])
                def14 = min(_def_base * def4 / 10000, def_pve_aura_max[_quality])

                hp13 = hp3 + hp14
                atk13 = atk3 + atk14
                def13 = def3 + def14
                s1 = '21,' + str(int(hp13)) + ';31,' + str(int(atk13)) + ';41,' + str(int(def13))

                hp5 = hp_pve_type_aura_limiter[_limiter]
                atk5 = atk_pve_type_aura_limiter[_limiter]
                def5 = def_pve_type_aura_limiter[_limiter]

                hp6 = hp_pve_type_aura_per_limiter[_limiter]
                atk6 = atk_pve_type_aura_per_limiter[_limiter]
                def6 = def_pve_type_aura_per_limiter[_limiter]

                hp16 = min(_hp_base * hp6 / 10000, hp_pve_type_aura_max[_quality])
                atk16 = min(_atk_base * atk6 / 10000, atk_pve_type_aura_max[_quality])
                def16 = min(_def_base * def6 / 10000, def_pve_type_aura_max[_quality])

                hp15 = hp5 + hp16
                atk15 = atk5 + atk16
                def15 = def5 + def16
                s2 = '21,' + str(int(hp15)) + ';31,' + str(int(atk15)) + ';41,' + str(int(def15))
            else:
                hp1 = hp_pvp_v_limiter[_limiter]
                atk1 = atk_pvp_v_limiter[_limiter]
                def1 = def_pvp_v_limiter[_limiter]

                hp2 = hp_pvp_per_limiter[_limiter]
                atk2 = atk_pvp_per_limiter[_limiter]
                def2 = def_pvp_per_limiter[_limiter]

                hp12 = min(_hp_base * hp2 / 10000, hp_pvp_max[_quality])
                atk12 = min(_atk_base * atk2 / 10000, atk_pvp_max[_quality])
                def12 = min(_def_base * def2 / 10000, def_pvp_max[_quality])

                hp11 = hp1 + hp12
                atk11 = atk1 + atk12
                def11 = def1 + def12

                hp3 = hp_pvp_aura_limiter[_limiter]
                atk3 = atk_pvp_aura_limiter[_limiter]
                def3 = def_pvp_aura_limiter[_limiter]

                hp4 = hp_pvp_aura_per_limiter[_limiter]
                atk4 = atk_pvp_aura_per_limiter[_limiter]
                def4 = def_pvp_aura_per_limiter[_limiter]

                hp14 = min(_hp_base * hp4 / 10000, hp_pvp_aura_max[_quality])
                atk14 = min(_atk_base * atk4 / 10000, atk_pvp_aura_max[_quality])
                def14 = min(_def_base * def4 / 10000, def_pvp_aura_max[_quality])

                hp13 = hp3 + hp14
                atk13 = atk3 + atk14
                def13 = def3 + def14
                s1 = '21,' + str(int(hp13)) + ';31,' + str(int(atk13)) + ';41,' + str(int(def13))

                hp5 = hp_pvp_type_aura_limiter[_limiter]
                atk5 = atk_pvp_type_aura_limiter[_limiter]
                def5 = def_pvp_type_aura_limiter[_limiter]

                hp6 = hp_pvp_type_aura_per_limiter[_limiter]
                atk6 = atk_pvp_type_aura_per_limiter[_limiter]
                def6 = def_pvp_type_aura_per_limiter[_limiter]

                hp16 = min(_hp_base * hp6 / 10000, hp_pvp_type_aura_max[_quality])
                atk16 = min(_atk_base * atk6 / 10000, atk_pvp_type_aura_max[_quality])
                def16 = min(_def_base * def6 / 10000, def_pvp_type_aura_max[_quality])

                hp15 = hp5 + hp16
                atk15 = atk5 + atk16
                def15 = def5 + def16
                s2 = '21,' + str(int(hp15)) + ';31,' + str(int(atk15)) + ';41,' + str(int(def15))

            _hp_limiter = hp11
            _hp_limiter_aura = hp13
            _hp_limiter_type_aura = hp15

            _atk_limiter = atk11
            _atk_limiter_aura = atk13
            _atk_limiter_type_aura = atk15

            _def_limiter = def11
            _def_limiter_aura = def13
            _def_limiter_type_aura = def15

            _aura_limiter = s1
            _type_aura_limiter = s2
        else:
            _hp_limiter = 0
            _hp_limiter_aura = 0
            _hp_limiter_type_aura = 0

            _atk_limiter = 0
            _atk_limiter_aura = 0
            _atk_limiter_type_aura = 0

            _def_limiter = 0
            _def_limiter_aura = 0
            _def_limiter_type_aura = 0

            _aura_limiter = ''
            _type_aura_limiter = ''

        _power_limiter = tools.get_power(_hp_limiter, _atk_limiter, _def_limiter)

        _hp_collection = 0
        _atk_collection = 0
        _def_collection = 0
        _hp_total_collection = 0
        _atk_total_collection = 0
        _def_total_collection = 0
        _crit_collection = 0
        _crit_res_collection = 0
        _precise_collection = 0
        _parry_collection = 0
        _dmg_res_collection = 0
        _pvp_addition = ''

        if _collection_break > 0:
            _hp_total_collection += df_collection_break.loc[_collection_break, '_total_hp_' + _type].sum()
            _atk_total_collection += df_collection_break.loc[_collection_break, '_total_atk_' + _type].sum()
            _def_total_collection += df_collection_break.loc[_collection_break, '_total_def_' + _type].sum()
            _pvp_addition = '1,1,' + str(df_collection_break.loc[_collection_break, '1,1,'].sum()) + \
                            ';2,1,' + str(df_collection_break.loc[_collection_break, '2,1,'].sum()) + \
                            ';3,1,' + str(df_collection_break.loc[_collection_break, '3,1,'].sum()) + \
                            ';4,1,' + str(df_collection_break.loc[_collection_break, '4,1,'].sum()) + \
                            ';1,2,' + str(df_collection_break.loc[_collection_break, '1,2,'].sum()) + \
                            ';2,2,' + str(df_collection_break.loc[_collection_break, '2,2,'].sum()) + \
                            ';3,2,' + str(df_collection_break.loc[_collection_break, '3,2,'].sum()) + \
                            ';4,2,' + str(df_collection_break.loc[_collection_break, '4,2,'].sum()) + \
                            ';5,1,' + str(df_collection_break.loc[_collection_break, '5,1,'].sum()) + \
                            ';5,2,' + str(df_collection_break.loc[_collection_break, '5,2,'].sum())

        if _collection_upgrade > 0:
            _hp_collection += df_collection_upgrade.loc[_collection_upgrade, '_hp_' + _type].sum()
            _atk_collection += df_collection_upgrade.loc[_collection_upgrade, '_atk_' + _type].sum()
            _def_collection += df_collection_upgrade.loc[_collection_upgrade, '_def_' + _type].sum()

        if _collection_collect > 0:
            _hp_collection += df_collection_collect.loc[_collection_collect, '_hp_' + _type].sum()
            _atk_collection += df_collection_collect.loc[_collection_collect, '_atk_' + _type].sum()
            _def_collection += df_collection_collect.loc[_collection_collect, '_def_' + _type].sum()
            _hp_total_collection += df_collection_collect.loc[_collection_collect, '_total_hp_' + _type].sum()
            _atk_total_collection += df_collection_collect.loc[_collection_collect, '_total_atk_' + _type].sum()
            _def_total_collection += df_collection_collect.loc[_collection_collect, '_total_def_' + _type].sum()
            _crit_collection += df_collection_collect.loc[_collection_collect, '_crit_' + _type].sum()
            _crit_res_collection += df_collection_collect.loc[_collection_collect, '_crit_res_' + _type].sum()
            _precise_collection += df_collection_collect.loc[_collection_collect, '_precise_' + _type].sum()
            _parry_collection += df_collection_collect.loc[_collection_collect, '_parry_' + _type].sum()
            _dmg_res_collection += df_collection_collect.loc[_collection_collect, '_dmg_res_' + _type].sum()

        _hp1 = _hp_base + _hp_equip + _hp_talent + _hp_academy + _hp_job + _hp_mechanical + _hp_limiter
        _atk1 = _atk_base + _atk_equip + _atk_talent + _atk_academy + _atk_job + _atk_mechanical + _atk_limiter
        _def1 = _def_base + _def_equip + _def_talent + _def_academy + _def_job + _def_mechanical + _def_limiter
        _crit1 = crit_init + _crit_equip + _crit_talent + _crit_job
        _crit_res1 = _crit_res_equip + _crit_res_talent + _crit_res_job
        _precise1 = _precise_equip + _precise_talent + _precise_job
        _parry1 = _parry_equip + _parry_talent + _parry_job
        _dmg_res1 = _dmg_res_equip + _dmg_res_talent + _dmg_res_job

        _hp = (_hp1 + _hp_collection) * (1 + _hp_total_collection / 10000)
        _atk = (_atk1 + _atk_collection) * (1 + _atk_total_collection / 10000)
        _def = (_def1 + _def_collection) * (1 + _def_total_collection / 10000)
        _crit = _crit1 + _crit_collection
        _crit_res = _crit_res1 + _crit_res_collection
        _crit_dmg = 15000
        _precise = _precise1 + _precise_collection
        _parry = _parry1 + _parry_collection
        _dmg_res = _dmg_res1 + _dmg_res_collection

        _power_collection = tools.get_power(_hp - _hp1, _atk - _atk1, _def - _def1, _crit_collection,
                                            _crit_res_collection,
                                            _precise_collection, _parry_collection, _dmg_res_collection)

        _power_total = tools.get_power(_hp, _atk, _def, _crit, _crit_res, _precise, _parry, _dmg_res)

        final_hp.append(_hp)
        final_atk.append(_atk)
        final_def.append(_def)
        final_crit.append(_crit)
        final_crit_res.append(_crit_res)
        final_crit_dmg.append(_crit_dmg)
        final_precise.append(_precise)
        final_parry.append(_parry)
        final_dmg_res.append(_dmg_res)
        final_aura.append(_aura_limiter)
        final_type_aura.append(_type_aura_limiter)

        power_base.append(_power_base)
        power_equip.append(_power_equip)
        power_talent.append(_power_talent)
        power_academy.append(_power_academy)
        power_job.append(_power_job)
        power_mechanical.append(_power_mechanical)
        power_limiter.append(_power_limiter)
        power_collection.append(_power_collection)
        power_total.append(_power_total)

        job_contact.append(_job_contact)
        pvp_addition.append(_pvp_addition)

        _level_list.append(_level)

    sv.save_hero_status(_id, _level_list, df_status, final_hp, final_atk, final_def, final_crit, final_crit_res,
                        final_crit_dmg, final_precise, final_parry, final_dmg_res, final_aura, final_type_aura,
                        power_base, power_equip, power_talent, power_academy, power_job, power_mechanical,
                        power_limiter, power_collection, power_total, _limiter_on, job_contact, pvp_addition)
