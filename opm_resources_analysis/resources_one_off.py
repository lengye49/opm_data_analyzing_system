from opm_spec_tools import opm_tools as tools
import pandas as pd

path = tools.get_version_path()


# 根据条件取前n行的值
def get_sum_rewards(_df, _col_name, _col_value):
    _rewards = {}
    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in _df.columns:
            _rewards[_t] = _df.loc[_df[_col_name] <= _col_value, _t].sum()
    return _rewards


def get_stage_rewards():
    df = tools.read_spec_file('Stage', path)
    df = tools.reset_rewards_to_dict(df, 'Reward')
    return get_sum_rewards(df, 'Id', stage)


def get_extreme_rewards():
    df = tools.read_spec_file('ExtremeSimulation', path)
    df = tools.reset_rewards_to_dict(df, 'Reward')
    _rewards = {}
    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in df.columns:
            _rewards[_t] += df.loc[(df['ExtremeType'] == 11) & (df['Floor'] < extreme_standard), _t].sum()
            _rewards[_t] += df.loc[((df['ExtremeType'] == 1) | (df['ExtremeType'] == 2) | (df['ExtremeType'] == 3)
                                    | (df['ExtremeType'] == 4)) & (df['Floor'] < extreme_race), _t].sum()
    return _rewards


def get_adventure_id(_id):
    new_id = int((_id - 100000) / 1000) + 1
    if new_id > 11:
        new_id -= 9
    return new_id


def get_adventure_rewards():
    df = tools.read_spec_file('MapUnit', path)
    df = df.drop(df[(df['Id'] > 500000) | (df['Id'] < 100000) | ((df['Type'] != 31) & (df['Type'] != 27))].index)
    df = df.reset_index()
    df['Adventure'] = df['Id'].apply(get_adventure_id)
    df = tools.reset_rewards_to_dict(df, 'Param3')
    return get_sum_rewards(df, 'Adventure', adventure)


def get_mission_rewards():  # _stage, _chapter, _extreme, _race_extreme, _days, _arena, _player_lv):
    df = tools.read_spec_file('Mission', path)
    df = tools.reset_rewards_to_dict(df, 'Reward')
    _rewards = {}
    for _t in rewards_type:
        _rewards[_t] = 0
        if _t in df.columns:
            # 类型1：通关
            _rewards[_t] += df.loc[(df['MissionType'] == 1) & (df['Target'] < stage), _t].sum()
            print(_rewards)
            # 类型2：拥有英雄数量
            _rewards[_t] += df.loc[(df['MissionType'] == 2) & (df['Target'] <= cards_count), _t].sum()
            print(_rewards)
            # 类型3：竞技场历史最大积分
            _rewards[_t] += df.loc[(df['MissionType'] == 3) & (df['Target'] <= arena_max_score), _t].sum()
            print(_rewards)
            # 类型4：竞技场胜利场数
            _rewards[_t] += df.loc[(df['MissionType'] == 4) & (df['Target'] <= arena_win_count), _t].sum()
            print(_rewards)
            # 类型5：通章
            _rewards[_t] += df.loc[(df['MissionType'] == 5) & (df['Target'] < chapter), _t].sum()
            print(_rewards)
            # 类型6：通关标准极限试炼
            _rewards[_t] += df.loc[(df['MissionType'] == 6) & (df['Target'] < extreme_standard), _t].sum()
            print(_rewards)
            # 类型35：通关类型极限试炼
            _rewards[_t] += df.loc[(df['MissionType'] == 35) & (df['Target'] < extreme_race), _t].sum()
            print(_rewards)
            # 类型7/      8/      10/     11/     12/     14/         19
            # Discord/Facebook/Twitter/Website/JoinGuild/1PurpleHero/OasisAccount
            _rewards[_t] += df.loc[(df['MissionType'] == 7) | (df['MissionType'] == 8) | (df['MissionType'] == 10)
                                   | (df['MissionType'] == 11) | (df['MissionType'] == 12) | (df['MissionType'] == 14)
                                   | (df['MissionType'] == 19), _t].sum()
            print(_rewards)
            # 类型13：挂机现金总量
            _rewards[_t] += df.loc[(df['MissionType'] == 13) & (df['Target'] <= afk_cash_count), _t].sum()
            print(_rewards)
            # 类型15：最大英雄等级
            _rewards[_t] += df.loc[(df['MissionType'] == 15) & (df['Target'] <= max_hero_level), _t].sum()
            print(_rewards)
            # 类型16：通关强者之路次数
            _rewards[_t] += df.loc[(df['MissionType'] == 16) & (df['Target'] <= (days / 2)), _t].sum()
            print(_rewards)
            # 类型17：共鸣水晶等级
            _rewards[_t] += df.loc[(df['MissionType'] == 17) & (df['Target'] <= connect_level), _t].sum()
            print(_rewards)
            # 类型18：共鸣水晶槽数
            _rewards[_t] += df.loc[(df['MissionType'] == 18) & (df['Target'] <= connect_holes), _t].sum()
            print(_rewards)
            # 类型20：队伍等级
            _rewards[_t] += df.loc[(df['MissionType'] == 20) & (df['Target'] <= player_level), _t].sum()
            print(_rewards)
    return _rewards


def get_mission_newbie_rewards():
    df = tools.read_spec_file('MissionNewbie', path)
    df = tools.reset_rewards_to_dict(df, 'Reward')
    # 默认达到天数即完成
    _rewards = get_sum_rewards(df, 'Day', days)
    return _rewards


def get_rank_rewards():
    df = tools.read_spec_file('Rank', path)
    df = tools.reset_rewards_to_dict(df, 'MissionReward')
    _rewards = get_sum_rewards(df, 'Id', 999999)
    # 排行榜奖励按天数发放 100天为上限
    for _t in _rewards:
        _rewards[_t] = int(_rewards[_t] * min(days / 100, 1.0))
    return _rewards


def get_seven_day_rewards():
    df = tools.read_spec_file('Configs', path)
    seven_day_reward = tools.get_specific_property(df, 'value', 'key', 'SevenDaysReward')
    _rs = seven_day_reward.split('#S#')
    df = pd.DataFrame(_rs, index=range(1, 8), columns=['Reward'])
    df['Day'] = range(1, 8)
    df = tools.reset_rewards_to_dict(df,'Reward')
    _rewards = get_sum_rewards(df, 'Day', days)
    return _rewards


# 获取特定值
# df.loc[df['Id'] == 1, 'hero_exp']
# 获取前n行的和
# df.loc[df['Id'] <= 2, 'hero_exp'].sum()


# 当前关卡
stage = 9999
chapter = 99
# adventure = chapter - 5
adventure = 12
extreme_standard = 9999
extreme_race = 9999

days = 999

player_level = 9999
max_hero_level = 9999
connect_level = 9999
connect_holes = 9999

rewards_type = ['diamond', 'hero_exp', 'coin', 'hero_powder', 'exp']
cards_count = 500
afk_cash_count = 999999999
arena_max_score = 1800
arena_win_count = 999
# print(get_adventure_rewards())
# print(get_extreme_rewards())
# print(get_rank_rewards())
# print(get_mission_newbie_rewards())
print(get_seven_day_rewards())