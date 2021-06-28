from random import randint
from opm_resources_analysis.spec_loader import SpecLoader


class Resource:
    def __init__(self, rewards='', amount=1):
        # 支持的构造方式：reward1, num1; reward2, num2
        # 支持pack

        self.dict_res = dict()

        rs = rewards.split(';')
        while len(rs) > 0:
            new_rs = []
            for r in rs:
                if r == '':
                    continue

                s = r.split(',')

                if s[0] == 'prop':
                    _type = s[0] + '_' + str(s[1])
                    _num = int(s[2])
                elif s[1] in ['hero', 'equip']:
                    _type = s[0] + '_' + str(s[1])
                    _num = 1
                elif s[0] == 'pack':
                    _ = self.unpack_reward(int(s[1]))
                    new_rs.append(_)
                    _type = 0
                    _num = 0
                else:
                    _type = s[0]
                    _num = int(s[1])
                if _type != 0:
                    if _type not in self.dict_res:
                        self.dict_res[_type] = 0
                    self.dict_res[_type] += _num
            rs = new_rs

    def __getitem__(self, item):
        return self.dict_res[item]

    def __setitem__(self, key, value):
        self.dict_res[key] = value

    def cost(self, res_cost):
        dict_tmp = self.dict_res.copy()
        for t, amount in res_cost.dict_res.items():
            if amount > 0:
                if t in dict_tmp and dict_tmp[t] >= amount:
                    dict_tmp[t] -= amount
                else:
                    return False

        self.dict_res = dict_tmp
        return True

    def gain(self, res_gain):
        for t, amount in res_gain.dict_res.items():
            if amount > 0:
                if t not in self.dict_res:
                    self.dict_res[t] = 0
                self.dict_res[t] += amount
        return

    @classmethod
    def unpack_reward(cls, pack_id):
        t, v = SpecLoader.get_pack(pack_id)
        if t == 1:
            return v
        else:
            return cls.get_random_item(v)

    @classmethod
    def get_random_item(cls, rewards):
        rewards = rewards.split(';')
        items = []
        weights = []
        for reward in rewards:
            if '|' in reward:
                _r = reward.split('|')
                items.append(_r[0])
                weights.append(int(_r[1]))
            else:
                items.append(reward)
                weights.append(1)

        r = randint(0, sum(weights) - 1)
        for i in (0, len(weights) - 1):
            if r < weights[i]:
                return items[i]
            else:
                r -= weights[i]
        return items[0]