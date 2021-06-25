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
            _rewards = SpecLoader.get_config_value('SevenDayReward')



if __name__ == '__main__':
    user = User(PlayerType.ZERO_PAY)

    list_output = []

    for i in range(Policy.day_limit):
        print(f'DAY {i}')

        user.user_res.set_cur_day(i)
        user.gain_daily_reward(i)