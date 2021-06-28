from enum import Enum

from opm_resources_analysis.policy import Policy
from opm_resources_analysis.hero import Hero
from opm_resources_analysis.user_resource import UserResource
from opm_resources_analysis.spec_loader import SpecLoader


class PlayerType(Enum):
    ZERO_PAY = 0
    SMALL_PAY = 1
    MEDIAN_PAY = 2
    BIG_PAY = 3
    HUGE_PAY = 4


class Formation:
    def __init__(self):
        self.heroes = []
        hero_ids = Policy.get_formation_heroes()
        for hero_id in hero_ids:
            self.heroes.append(Hero(hero_id))
        return


class User:
    def __init__(self, player_type):
        self.player_type = player_type

        self.tower = 1
        self.stage = 1

        self.user_res = UserResource()
        self.formation = Formation()

        self.mission_stage = 0

    def gain_daily_reward(self, day):   # 获取每日上线奖励
        if day < 7:
            res = SpecLoader.get_seven_day_reward(day)
            self.user_res.gain(res, '七日奖励')

        self.get_arena_daily_rewards()
        self.get_commission_reward(day)
        self.get_daily_mission_reward(day)
        if day % 14 == 0:
            self.get_arena_season_rewards()

    def get_arena_daily_rewards(self):
        for i in range(0, Policy.daily_arena_count):
            res = SpecLoader.get_arena_battle_rewards()
            self.user_res.gain(res, '竞技场参与奖励')
        res = SpecLoader.get_arena_daily_reward(Policy.arena_rank_interval)
        self.user_res.gain(res, '竞技场排行奖励')

    def get_arena_season_rewards(self):
        res = SpecLoader.get_arena_season_reward(Policy.arena_rank_interval)
        self.user_res.gain(res, '竞技场结算奖励')

    def get_commission_reward(self, day):
        lv = Policy.get_commission_level(day)
        for i in range(0, Policy.commission_count_solo()):
            res = SpecLoader.get_commission_reward(lv, 1)
            self.user_res.gain(res, '委托')
        for i in range(0, Policy.commission_count_team()):
            res = SpecLoader.get_commission_reward(lv, 2)
            self.user_res.gain(res, '委托')

    def get_daily_mission_reward(self, day):
        # 日常
        res = SpecLoader.get_daily_mission_reward(Policy.daily_activity, 0)
        self.user_res.gain(res, '日常任务')
        # 周常
        last_week_activity = (day % 7 - 1) * Policy.daily_week_activity
        week_day = 7 if (day % 7 == 0) else (day % 7)
        week_day_activity = week_day * Policy.daily_week_activity
        res = SpecLoader.get_weekly_mission_reward(last_week_activity, week_day_activity)
        self.user_res.gain(res, '日常任务')

    # todo get_guild_boss_reward
    # todo get_ads_reward
    # todo get_battle_pass_reward
    # todo get_big_monster_reward
    # todo get_daily_giftpack_reward
    # todo get_draw_card_reward 累计奖励
    # todo get_friend_draw_card_reward 友情抽卡奖励
    # todo get_growth_fund_reward
    # todo get_labyrinth_reward
    # todo get_adventure_reward
    # todo get_wonderful_journey_reward 每两周一轮 5-40后开启
    # todo get_mission_reward
    # todo get_mission_newbie_reward
    # todo get_prop_reward 每日最后的时候使用道具获取资源
    # todo get_shop_reward
    # todo get_stage_reward
    # todo get_stage_afk_reward
    # todo get_extreme_simulation_reward
    # todo get_training_stage_reward
    # todo check_unlock



if __name__ == '__main__':
    user = User(PlayerType.ZERO_PAY)

    list_output = []

    for i in range(Policy.day_limit):
        print(f'DAY {i}')

        user.user_res.set_cur_day(i)
        user.gain_daily_reward(i)