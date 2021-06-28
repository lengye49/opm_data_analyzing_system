from random import randint
from opm_resources_analysis.utils import load_specs
from opm_resources_analysis.resource import Resource


class SpecLoader:
    df_hero = load_specs('Hero')

    df_configs = load_specs('Configs')
    df_configs = df_configs.rename(columns={'Unnamed: 2': 'Key'})

    df_reward = load_specs('Reward')

    df_arena_rank_reward = load_specs('ArenaNormalRankReward')

    df_commission = load_specs('Commission')
    df_commission['coin'] = df_commission['CoinAfkTime'].apply(lambda x: 'prop,402,' + str(x / 7200))

    df_commission_lv = load_specs('CommissionLevel')

    df_daily_mission = load_specs('MissionDailyReward')

    @classmethod
    def get_config_value(cls, key):
        return cls.df_configs.loc[cls.df_configs['Key'] == key, 'Value'].values[0]

    @classmethod
    def get_seven_day_reward(cls, day):
        rewards = cls.get_config_value('SevenDayReward').split('#S#')[day - 1]
        return Resource(rewards)

    @classmethod
    def get_arena_battle_rewards(cls):
        rewards = cls.get_config_value('ArenaWinnerReward')
        return Resource(rewards)

    @classmethod
    def get_pack(cls, pack_id):
        t = int(cls.df_reward.loc[cls.df_reward['Id'] == pack_id, 'Type'].values[0])
        v = cls.df_reward.loc[cls.df_reward['Id'] == pack_id, 'Value'].values[0]
        return t, v

    @classmethod
    def get_arena_daily_reward(cls, rank_id):
        rewards = cls.df_arena_rank_reward.loc[cls.df_arena_rank_reward['Id'] == rank_id, 'DailyReward']
        return Resource(rewards)

    @classmethod
    def get_arena_season_reward(cls, rank_id):
        rewards = cls.df_arena_rank_reward.loc[cls.df_arena_rank_reward['Id'] == rank_id, 'SeasonReward']
        return Resource(rewards)

    @classmethod
    def get_commission_reward(cls, lv, commission_type):
        # commission_type: 1 solo, 2 team
        quality = cls.get_commission_quality(lv, commission_type)
        _df = cls.df_commission.loc[
            cls.df_commission['CommissionLevel'] == quality & cls.df_commission['Type'] == commission_type]
        ids = list(_df['Id'])
        _id = randint(0, len(ids) - 1)
        r = randint(0, 1)
        if r == 0:
            rewards = _df.loc[_df['Id'] == _id, 'Reward']
        else:
            rewards = _df.loc[_df['Id'] == _id, 'coin']
        return Resource(rewards)

    @classmethod
    def get_commission_quality(cls, lv, commission_type):
        # 根据委托等级获得实际的任务品质
        if commission_type==1:
            weight = cls.df_commission_lv.loc[cls.df_commission_lv['Id'] == lv, 'CommissionWeight']
        else:
            weight = cls.df_commission_lv.loc[cls.df_commission_lv['Id'] == lv, 'CommissionWeightTeam']
        return cls.get_item_by_weight(weight)

    @classmethod
    def get_item_by_weight(cls, ws):
        ws = ws.split(';')
        items = []
        weights = []
        for w in ws:
            _ = w.split(',')
            items.append(int(_[0]))
            weights.append(int(_[1]))
        r = randint(0, sum(weights) - 1)

        for i in (0, len(weights) - 1):
            if r < weights[i]:
                return items[i]
            else:
                r -= weights[i]
        return items[0]

    @classmethod
    def get_daily_mission_reward(cls, activity, _type=0):
        # _type: 0 daily, 1 weekly
        reward = ''
        x = int(activity / 20) + 1
        for i in range(1,x):
            _id = (_type + 1) * 100 + i
            reward += ';' + cls.df_daily_mission.loc[cls.df_daily_mission['Id'] == _id, 'Reward']
        return Resource(reward)

    @classmethod
    def get_weekly_mission_reward(cls, start, end):
        s = int(start / 20) + 1
        e = int(end / 20) + 1
        reward = ''
        for i in range(s, e):
            _id = 200 + i
            reward += ';' + cls.df_daily_mission.loc[cls.df_daily_mission['Id'] == _id, 'Reward']
        return Resource(reward)