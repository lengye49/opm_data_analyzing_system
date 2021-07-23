#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author cn_sky
import json
import requests
import time
import threading
import datetime
import random


def ding_talk(content=''):
    url = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=583a8ee9420b1d0fe980dc2133b04fb1c3955d6cfb61469b7d2f0cc40e02dd29 '

    # url = 'https://oapi.dingtalk.com/robot/send?access_token' \
    #       '=786b6e320aa4bc4889d5924c014b1b68d31f6d90e116d4597e347cbae655020c '

    content = '起来嗨:\n' + content
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    data = {"msgtype": "text",
             "text": {
                 "content": content
             },
             "at": {
                 "atMobiles": [

                 ],
                 "isAtAll": True
             }
             }

    # print(json.dumps(data))
    result = requests.post(url, data=json.dumps(data), headers=headers)
    print(result.text)


def get_rand_player():
    return players[random.randint(0,len(players)-1)]


def check_time():
    now_hour = time.localtime().tm_hour

    global last_hour
    if now_hour in [11, 15, 17] and last_hour != now_hour:
        if last_hour == 0:
            ding_talk(update_language)
        else:
            standard_day = datetime.date(2021, 6, 13)
            curr_day = datetime.date.today()
            w = (curr_day - standard_day).days % 7
            s = '这一轮有请 -->' + get_rand_player() + '<-- 带头锻炼！\n\n'
            if w in [1, 2, 3, 4, 5]:
                ding_talk('到点了！\n\n来呀，动起来！Come On Baby！\n\n' + s)
            else:
                print('weekend.')

    last_hour = now_hour


def timer_task():
    print(time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
    # ding_talk(update_language)
    check_time()

    global timer
    timer = threading.Timer(300, timer_task)
    timer.start()


last_hour = 0
players = ['苏成峰', '郑勇', '李涵笑', '范哲源', '王时雨', '徐海华', '刘永南', '王沛鸿']
update_language = '小宝更新：周末不再打扰大家休息。\n\n另外，欢迎新成员 - 石雨欣<妹子！>\n\n计时重新开始！'

if __name__ == "__main__":
    timer = threading.Timer(2, timer_task)
    timer.start()

