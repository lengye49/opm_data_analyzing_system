#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author cn_sky
import json
import requests
import time
import threading

def ding_talk(content=''):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=583a8ee9420b1d0fe980dc2133b04fb1c3955d6cfb61469b7d2f0cc40e02dd29'
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
                 "isAtAll": False
             }
             }

    # print(json.dumps(data))
    result = requests.post(url, data=json.dumps(data), headers=headers)
    print(result.text)


def check_time():
    print('checking', time.localtime())
    now_day = time.strftime('%Y%m%d', time.localtime())

    # 节假日接口(工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2 )
    server_url = "http://www.easybots.cn/api/holiday.php?d="
    req = requests.get(server_url + now_day)
    vop_data = json.loads(req.text)

    now_hour = time.localtime().tm_hour

    global last_hour
    if now_hour in [10, 11, 15, 17] and last_hour != now_hour:
        if int(vop_data[now_day]) == 0:
            ding_talk('到点了！\n\n来呀，动起来！Come On Baby！')
        elif int(vop_data[now_day]) == 1:
            ding_talk('到点了！\n\n虽然是周末，也不要懈怠哦！动起来吧！')
        elif int(vop_data[now_day]) == 2:
            ding_talk('到点了！\n\n假期怎么能少了锻炼，快动起来吧！来一组！')
        else:
            print('connect error!')
    last_hour = now_hour
    # print('last_hour', last_hour)


def timer_task():
    print(time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
    check_time()

    global timer
    timer= threading.Timer(300, timer_task)
    timer.start()


last_hour = 0

if __name__ == "__main__":
    timer = threading.Timer(2, timer_task)
    timer.start()

