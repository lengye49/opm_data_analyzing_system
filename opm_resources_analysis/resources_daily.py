import pandas as pd
from opm_spec_tools import opm_tools as tools
import numpy as np
import math


def get_vip_bonus():
    _df = tools.read_spec_file('Vip', path)
    _df = tools.reset_dict_str_to_dict(_df, 'Properties')
    return tools.get_specific_property(_df, '1', 'Level', vip)


def get_stage_afk_rewards():
    _df = tools.read_spec_file('StageAfk', path)
    exp_rate = tools.get_specific_property(_df, 'Exp', 'Id', stage)
    coin_rate = tools.get_specific_property(_df, 'Coin', 'Id', stage)
    hero_exp_rate = tools.get_specific_property(_df, 'HeroExp', 'Id', stage)
    powder_rate = tools.get_specific_property(_df, 'Powder', 'Id', stage)

    # vip加成
    _bonus = int(get_vip_bonus())
    _rewards = {'hero_exp': int(hero_exp_rate / 10000 * 86400 * days * (10000 + _bonus) / 10000),
                'coin': int(coin_rate / 10000 * 86400 * days * (10000 + _bonus) / 10000),
                'exp': int(exp_rate / 10000 * 86400 * days),
                'hero_powder': int(powder_rate / 10000 * 86400 * days)}
    # 快速挂机奖励
    _rewards['hero_exp'] += int(hero_exp_rate / 10000 * 7200 * daily_quick_afk_times * days * (10000 + _bonus) / 10000)
    _rewards['coin'] += int(coin_rate / 10000 * 7200 * daily_quick_afk_times * days * (10000 + _bonus) / 10000)
    _rewards['hero_powder'] += int(powder_rate / 10000 * 7200 * daily_quick_afk_times * days)
    return _rewards


def get_daily_mission_rewards():
    _df = tools.read_spec_file('MissionDailyReward', path)
    _df = tools.reset_rewards_to_dict(_df, 'Reward')
    _rewards = {}
    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in _df.columns:
            _rewards[_t] += int(
                _df.loc[(_df['DailyType'] == 0) & (_df['ActivityRequire'] <= daily_mission_progress), _t].sum() * days)
            _rewards[_t] += int(_df.loc[(_df['DailyType'] == 1) & (
                    _df['ActivityRequire'] <= weekly_mission_progress), _t].sum() * weeks)
    return _rewards


def get_battle_pass_rewards():
    _df = tools.read_spec_file('BattlePass', path)
    # 免费奖励
    _df1 = tools.reset_rewards_to_dict(_df, 'NormalReward')
    # 付费奖励
    _df2 = tools.reset_rewards_to_dict(_df, 'PaidReward')
    _rewards = {}
    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in _df1.columns:
            # 将通行证统一处理为45天，免费奖励用1级，付费奖励用5级
            _rewards[_t] += int(
                _df1.loc[(_df1['PassLevel'] == 1) & (_df1['Level'] <= battle_pass_level), _t].sum() * days / 45)
            if is_buy_battle_pass:
                _rewards[_t] += int(
                    _df2.loc[(_df2['PassLevel'] == 5) & (_df2['Level'] <= battle_pass_level), _t].sum() * days / 45)
    return _rewards


def get_commission_separate_rewards(_df, _days, _lv, _lv_team):
    _df1 = pd.DataFrame(_df[_df['Type'] == 1]).set_index('CommissionLevel').drop(['Type', 'index'], axis=1)
    _df2 = pd.DataFrame(_df[_df['Type'] == 2]).set_index('CommissionLevel').drop(['Type', 'index'], axis=1)

    _s1 = pd.Series(_lv).apply(int)
    _s1.index = _s1.index.astype(int)
    _s1.index.name = 'CommissionLevel'

    _s2 = pd.Series(_lv_team).apply(int)
    _s2.index = _s2.index.astype(int)
    _s2.index.name = 'CommissionLevel'

    _df1 = _df1.mul(_s1, axis=0) / _s1.sum()
    _df2 = _df2.mul(_s2, axis=0) / _s2.sum()

    _rewards = {}

    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in _df1.columns:
            _rewards[_t] = _df1[_t].sum() / 2 * days
        if _t in _df2.columns:
            _rewards[_t] = _df2[_t].sum() / 2 * days

    return _rewards


def separate_commission(_df, _max, _min, _lv=None, _lv_team=None):
    if days < _min:
        return {}

    if days <= _max:
        return get_commission_separate_rewards(_df, days - _min, _lv, _lv_team)
    else:
        return get_commission_separate_rewards(_df, _max - _min, _lv, _lv_team)


def get_commission_rewards():
    _df = tools.read_spec_file('Commission', path)

    # 将金币奖励改为2小时金币奖励，要奖励结果/7200
    _df['coin'] = ';prop,402,'
    _df['Reward'] = _df['Reward'] + _df['coin'] + _df['CoinAfkTime'].map(str)
    _df = tools.reset_rewards_to_dict(_df, 'Reward')
    if 'prop_402' in _df.columns:
        _df['prop_402'] /= 7200

    # 将统一委托等级下的各种奖励取平均，方便计算
    _df = _df.groupby(['CommissionLevel', 'Type']).mean().fillna(0).reset_index()  # 计算的结果要除以2，因为要跟金币平分概率

    # 通过委托等级表，拆分出各个等级下刷新不同委托任务的权重
    _df_lv = tools.read_spec_file('CommissionLevel', path)
    _df_lv = tools.reset_dict_str_to_dict(_df_lv, 'CommissionWeight')
    _df_lv.drop(_df_lv.columns.difference(['CommissionLevel', 'CommissionWeight', 'CommissionWeightTeam']), axis=1,
                inplace=True)
    _df_lv = tools.reset_dict_str_to_dict(_df_lv, 'CommissionWeightTeam')
    _df_lv.drop(_df_lv.columns.difference(['CommissionLevel', 'CommissionWeight', 'CommissionWeightTeam']), axis=1,
                inplace=True)

    # 根据不同天数对应的委托等级，计算委托奖励
    # 等级与天数对应：5:2;14:3;39,4;89,5;152,6;195,7;99999,8
    _rewards = separate_commission(_df, 5, 0, _df_lv['CommissionWeight'][1], _df_lv['CommissionWeightTeam'][1])
    _rewards = tools.combine_dict(_rewards, separate_commission(_df, 14, 5, _df_lv['CommissionWeight'][2],
                                                                _df_lv['CommissionWeightTeam'][2]))
    _rewards = tools.combine_dict(_rewards, separate_commission(_df, 39, 14, _df_lv['CommissionWeight'][3],
                                                                _df_lv['CommissionWeightTeam'][3]))
    _rewards = tools.combine_dict(_rewards, separate_commission(_df, 89, 39, _df_lv['CommissionWeight'][4],
                                                                _df_lv['CommissionWeightTeam'][4]))
    _rewards = tools.combine_dict(_rewards, separate_commission(_df, 152, 89, _df_lv['CommissionWeight'][5],
                                                                _df_lv['CommissionWeightTeam'][5]))
    _rewards = tools.combine_dict(_rewards, separate_commission(_df, 195, 152, _df_lv['CommissionWeight'][6],
                                                                _df_lv['CommissionWeightTeam'][6]))
    _rewards = tools.combine_dict(_rewards, separate_commission(_df, 999999, 195, _df_lv['CommissionWeight'][7],
                                                                _df_lv['CommissionWeightTeam'][7]))
    return _rewards


def get_arena_rewards():
    data = {'coin': 90000, 'hero_powder': 10}
    _df = pd.DataFrame(data, index=[1])

    _rewards = {}
    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in _df.columns:
            _rewards[_t] += _df[_t].sum() * 5 * days / 2
    return _rewards


rewards_type = ['diamond', 'hero_exp', 'coin', 'hero_powder', 'exp', 'prop_402']

vip = 8
stage = 349
path = tools.get_version_path()
days = 100
weeks = math.ceil(days / 7)
daily_mission_progress = 100
weekly_mission_progress = 100
daily_quick_afk_times = 2

# 委托临时
personal_commission_count = 5
team_commission_count = 1

battle_pass_level = 25
is_buy_battle_pass = True

# print(get_vip_bonus())
# print(get_stage_afk_rewards())
# print(get_daily_mission_rewards())
# print(get_battle_pass_rewards())
# print(get_commission_rewards())
print(get_arena_rewards())
