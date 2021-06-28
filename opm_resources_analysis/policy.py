class Policy:
    formation = '1, 2, 49, 115, 101'  # 培养阵容
    day_limit = 14  # 游戏天数
    daily_arena_count = 5  # 每日参与竞技场次数
    arena_rank_interval = 5  # 竞技场排名分段
    commission_levels = [0, 0, 5, 14, 39, 89, 152, 195, 99999]  # 委托天数设定
    commission_count = [5, 1]   # 个人/团队委托任务初始数量
    is_subscribe = False    # 是否订阅
    daily_activity = 100
    daily_week_activity = 20

    @classmethod
    def get_formation_heroes(cls):
        heroes = cls.formation.split(',')
        ret = [int(h) for h in heroes]
        return ret

    @classmethod
    def get_commission_level(cls, day):
        for i in range(0, len(cls.commission_levels)):
            if day < cls.commission_levels[i]:
                return i
        return 8

    @classmethod
    def commission_count_solo(cls, vip=0):
        return cls.commission_count[0]

    @classmethod
    def commission_count_team(cls, vip=0):
        return cls.commission_count[1] + (1 if cls.is_subscribe else 0)
