# 这个表的目标是判断某个阶段玩家应该购买什么类型的礼包
# 目前只考虑了giftpack相关的产出，未考虑基金、通行证、月卡、周卡、轮换活动等系列产出
# 目前尚未考虑各礼包限制条件及玩家所处状态

import pandas as pd


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
    result = {'Total': total_value, 'Ratio': total_value/vip}
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
    return total_value/v


def get_order_key(_dict):
    if order_key in _dict:
        return _dict[order_key]
    else:
        return 0


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
giftpack = giftpack.fillna(0)   # 将NAN值改为0

# 获取礼包报价
giftpack['Price'] = giftpack['Id'].apply(get_price)
giftpack['Vip'] = giftpack['Price'].apply(get_basic_vip)

# 分类处理Giftpack的奖励
s = giftpack.apply(lambda g: get_rewards(g['MainStageReward'], str(g['DesireList']), g['ChooseReward'], g['Vip'],
                                         g['Id']), axis=1)
s.name = 'Contents'
giftpack = giftpack.join(s)

# 清理GiftPack
giftpack = giftpack.drop(
    ['Order', 'Name', 'Icon', 'Reward', 'RewardPreview', 'Desire', 'DesirePos', 'DefaultShow', 'NextId', 'IsFree',
     'Value', 'Prefab', 'DiamondDes', 'IconBg', 'HotVisible', 'VisibleCondition', 'ExtraPurchaseTimes', 'ImgSource',
     'Server', 'MainStage', 'MainStageRewardPreview', 'MainStageReward', 'Version', 'ChooseIdx', 'DesireList',
     'ChooseReward'], axis=1)

order_key = '品质_ratio'

# GiftPack按某个值排序
while True:
    req = input('选择当前缺少的资源类型:等级,品质,装备,天赋,职阶,限制器,机器人,机械核心,其它\n')
    if req in ['等级','品质','装备','天赋','职阶','限制器','机器人','机械核心','其它']:
        order_key = req + '_ratio'
        giftpack['order_key'] = giftpack['Contents'].apply(get_order_key)
        giftpack = giftpack.sort_values(by='order_key', ascending=False)
        print(giftpack.head(10))
