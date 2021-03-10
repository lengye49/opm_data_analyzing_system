# 用于属性的通用配置

PowerParamHp = 1
PowerParamAtk = 6.9
PowerParamDef = 5.75
PowerParamCrit = 1.65
PowerParamCritRes = 1.65
PowerParamCritBonus = 0
PowerParamParry = 0.85
PowerParamPrecise = 0.85
PowerParamDmgRes = 1.75
PowerParamFury = 0


def get_grade(level):
    """
    根据英雄等级计算品阶
    :param level:
    :return:
    """
    if level <= 10:
        return 1
    else:
        return min(19, int((level - 1) / 20) + 2)


def get_real_level(level, enhance):
    """
    根据展示等级和强化等级计算实际等级
    :param level:
    :param enhance:
    :return:
    """
    if level < 240:
        return level
    else:
        return (level - 240) * 10 + 240 + enhance


def get_pvp_level(_l):
    """
    计算角色的竞技等级
    :param _l:
    :return:
    """
    return 240 + int(_l / 10)


def get_power(_hp=0, _atk=0, _def=0, _crit=0, _crit_res=0, _precise=0, _parry=0, _dmg_res=0):
    power = 0
    power += _hp * PowerParamHp
    power += _atk * PowerParamAtk
    power += _def * PowerParamDef
    power += _crit * PowerParamCrit
    power += _crit_res * PowerParamCritRes
    power += _precise * PowerParamPrecise
    power += _parry * PowerParamParry
    power += _dmg_res * PowerParamDmgRes
    return power
