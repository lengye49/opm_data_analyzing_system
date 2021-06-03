# 这个脚本的目标是判断某个阶段玩家在缺某种类型的资源时应该在哪里付费
# 目前只考虑了giftpack相关的产出，todo 基金、通行证、月卡、周卡等系列产出
# todo 各礼包限制条件及玩家所处状态和可购买次数限制
# 目前尚未考虑活动道具转换为目标资源的途径

import pandas as pd
from datetime import datetime


def is_on_time(start, end):
    # 判断礼包是否还是时间段内
    start = str(start)
    end = str(end)

    _t = datetime.strptime(target_time, '%Y%m%d')
    if start != '0':
        _s = datetime.strptime(start, '%Y%m%d%H%M')
        if _t < _s:
            return False
    if end != '0':
        _e = datetime.strptime(end, '%Y%m%d%H%M')
        if _t > _e:
            return False

    return True


def check_reward_type(reward):
    # 拆分reward字段

    s = reward.split(',')
    if s[0] == 'prop':
        _id = int(s[1])
        count = int(s[2])
        _type = prop.loc[_id, 'type']
        value = prop.loc[_id, 'value'] * count
        return _type, value

    elif s[0] == 'hero':
        _id = int(s[1])
        _type = '品质'
        value = hero.loc[_id, 'value']
        if len(s) > 2:
            if s[2] == '6':
                value *= 2
        return _type, value

    elif s[0] == 'equip':
        _id = int(s[1])
        _type = '装备'
        value = equip.loc[_id, 'value']
        return _type, value

    elif s[0] == 'vip_exp':
        return 'vip_exp', int(s[1])

    else:
        _type = resource.loc[s[0], 'type']
        value = resource.loc[s[0], 'value'] * int(s[1])
        return _type, value


def check_desire_type(desire_id):
    # 拆分desire奖励
    _type = desire.loc[desire_id, 'type']
    value = desire.loc[desire_id, 'value']
    return _type, value


def check_choose_type(choose_id):
    # 拆分choose奖励
    _type = choose.loc[choose_id, 'type']
    value = choose.loc[choose_id, 'value']
    return _type, value


def cal_type_percentage(_dict, vip, _id):
    # 计算各类型奖励占比
    total_value = 0
    for k in _dict.keys():
        if k != 'vip_exp':
            total_value += _dict[k]

    # 总价值与总性价比
    result = {'Total': total_value, 'Ratio': total_value / vip}
    # '等级%': 0, '品质%': 0, '装备%': 0, '天赋%': 0, '职阶%': 0, '限制器%': 0, '机器人%': 0, '机械核心%': 0, '其它%': 0}

    for k in _dict:
        result[k] = _dict[k]

    for k in _dict:
        ks = k.split('|')
        for _k in ks:
            if _k == 'vip_exp':
                if _dict[_k] != vip:
                    print(_id, 'Vip Dis-Match!')
            else:
                # 价值占比 及 分类性价比
                result[_k + '%'] = _dict[k] / total_value
                result[_k + '_ratio'] = _dict[k] / vip

    return result


def update_dict(_dict, k, v):
    if k in _dict:
        _dict[k] += v
    else:
        _dict[k] = v
    return _dict


def get_rewards(rewards, desires, chooses, vip, _id):
    r = {}

    if rewards != '0' and rewards != 0:
        if '#S#' in rewards:
            rewards = rewards.split('#S#')[0]
        s = rewards.split(';')

        for ss in s:
            k, v = check_reward_type(ss)
            r = update_dict(r, k, v)

    if desires != '0':
        s = desires.split(',')
        for ss in s:
            k, v = check_desire_type(int(ss))
            r = update_dict(r, k, v)

    if chooses != 0:
        k, v = check_choose_type(chooses)
        r = update_dict(r, k, v)

    r = cal_type_percentage(r, vip, _id)
    return r


def get_price(_id):
    price = 0
    try:
        price = commodity.loc[_id * 10, 'price']
    finally:
        return price


def get_basic_vip(price):
    price = float(price)
    return ratio.loc[price, 'vip_exp']


def get_cost_performance(total_value, price):
    v = ratio.loc[price, 'vip_exp']
    return total_value / v


def get_order_key(_dict):
    if order_key in _dict:
        return _dict[order_key]
    else:
        return 0


order_key = '品质_ratio'
target_time = '20200505'

prop = pd.read_excel('resource_types.xlsx', header=0, sheet_name='prop', index_col=0)
prop.dropna(axis=0, how='all')  # 删除空行
prop = prop.fillna('未知')

hero = pd.read_excel('resource_types.xlsx', header=0, sheet_name='hero', index_col=0)
hero.dropna(axis=0, how='all')  # 删除空行
hero = hero.fillna('未知')

equip = pd.read_excel('resource_types.xlsx', header=0, sheet_name='equip', index_col=0)
equip.dropna(axis=0, how='all')  # 删除空行
equip = equip.fillna('未知')

desire = pd.read_excel('resource_types.xlsx', header=0, sheet_name='desire', index_col=0)
desire.dropna(axis=0, how='all')  # 删除空行
desire = desire.fillna('未知')

choose = pd.read_excel('resource_types.xlsx', header=0, sheet_name='choose', index_col=0)
choose.dropna(axis=0, how='all')  # 删除空行
choose = choose.fillna('未知')

resource = pd.read_excel('resource_types.xlsx', header=0, sheet_name='others', index_col=0)
resource.dropna(axis=0, how='all')  # 删除空行
resource = resource.fillna('未知')

ratio = pd.read_excel('resource_types.xlsx', header=0, sheet_name='ratio', index_col=0)
ratio.dropna(axis=0, how='all')  # 删除空行

commodity = pd.read_excel('Commodity.xlsx', header=2, sheet_name='Commodity', index_col=0)
commodity.dropna(axis=0, how='all')  # 删除空行
commodity = commodity.drop(['id'])  # 删除中文标示
commodity = commodity.drop(['Platform', 'ProductId', 'CurrencyPrice', 'Tier'], axis=1)

giftpack = pd.read_excel('GiftPack.xlsx', header=2, sheet_name='GiftPack')
giftpack.dropna(axis=0, how='all')  # 删除空行
giftpack = giftpack.drop([0])  # 删除中文标示
giftpack = giftpack.fillna(0)  # 将NAN值改为0

# 获取礼包报价
giftpack['Price'] = giftpack['Id'].apply(get_price)
giftpack['Vip'] = giftpack['Price'].apply(get_basic_vip)

# 分类处理Giftpack的奖励
s = giftpack.apply(lambda g: get_rewards(g['MainStageReward'], str(g['DesireList']), g['ChooseReward'], g['Vip'],
                                         g['Id']), axis=1)
s.name = 'Contents'
giftpack = giftpack.join(s)

# 去掉时间不符合的礼包
giftpack['OnTime'] = giftpack.apply(lambda g: is_on_time(g['StartTime'], g['EndTime']), axis=1)
giftpack = giftpack.drop(giftpack[giftpack['OnTime'] == False].index)

# 去掉关卡不符合的礼包

# 清理GiftPack
giftpack = giftpack.drop(
    ['Order', 'Name', 'Icon', 'Reward', 'RewardPreview', 'Desire', 'DesirePos', 'DefaultShow', 'NextId', 'IsFree',
     'Value', 'Prefab', 'DiamondDes', 'IconBg', 'HotVisible', 'VisibleCondition', 'ExtraPurchaseTimes', 'ImgSource',
     'Server', 'MainStage', 'MainStageRewardPreview', 'MainStageReward', 'Version', 'ChooseIdx', 'DesireList',
     'ChooseReward',], axis=1)

# ['Id', 'Type', 'SubType', 'TimeType', 'PurchaseTimes', 'StartTime', 'EndTime', 'Note', 'Price', 'Vip', 'Contents']
month_card1 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
               'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
month_card2 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
               'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
growth_fund1 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
                'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
growth_fund2 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
                'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
growth_fund3 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
                'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
battle_pass_1 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
                 'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
battle_pass_2 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
                 'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
battle_pass_3 = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
                 'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
hero_card = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
             'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
week_card = {'Id': 1, 'Type': 0, 'SubType': 0, 'TimeType': 0, 'PurchaseTimes': 0, 'StartTime': 0, 'EndTime': 0,
             'Note': 0, 'Price': 0, 'Vip': 0, 'Contents': 0}
other_packs = pd.DataFrame([month_card1, month_card2, growth_fund1, growth_fund2, growth_fund3, battle_pass_1,
                            battle_pass_2, battle_pass_3, week_card])

# GiftPack按某个值排序
while True:
    req = input('选择当前缺少的资源类型:等级,品质,装备,天赋,职阶,限制器,机器人,机械核心,其它\n')
    if req in ['等级', '品质', '装备', '天赋', '职阶', '限制器', '机器人', '机械核心', '其它']:
        order_key = req + '_ratio'
        giftpack['order_key'] = giftpack['Contents'].apply(get_order_key)
        giftpack = giftpack.sort_values(by='order_key', ascending=False)
        print(giftpack.head(10))
