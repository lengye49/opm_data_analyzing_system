import copy
from opm_resources_analysis.resource import Resource


class UserResource:
    def __init__(self):
        self.__cur_day = -1
        self.__dict_gain_history = dict()
        self.__dict_remain_history = dict()

        self.resource = Resource()

    def set_cur_day(self, day):
        if self.__cur_day < day:    # 当日期发生变更时，记录前一天剩余资源
            self.__dict_remain_history[self.__cur_day] = copy.deepcopy(self.resource)
            self.__cur_day = day
        else:
            raise RuntimeError(f'Error cur day: {day} __cur_day: {self.__cur_day}')
