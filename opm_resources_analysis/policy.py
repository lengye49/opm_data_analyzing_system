class Policy:
    formation = '1, 2, 49, 115, 101'    # 培养阵容
    day_limit = 14  # 游戏天数

    @classmethod
    def get_formation_heroes(cls):
        heroes = cls.formation.split(',')
        ret = [int(h) for h in heroes]
        return ret