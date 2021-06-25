class Resource:
    def __init__(self, rewards='', amount=1):
        # 支持的构造方式：reward1, num1; reward2, num2

        self.dict_res = dict()

        rs = rewards.split(';')

        for r in rewards:
            s = r.split(',')
            if s[0] == 'prop':
                _type = s[0] + '_' + str(s[1])
                _num = int(s[2])
            else:
                _type = s[0]
                _num = int(s[1])

            if _type not in self.dict_res:
                self.dict_res[_type] = 0
            self.dict_res[_type] += _num

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

