#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author sky
import requests
import json
import time


def ding_talk(_t='text'):
    headers = {
        "Content-Type": "application/json"
    }
    data1 = {"msgtype": "text",
             "text": {
                 "content": "python警告:\nLet's go!"
             },
             "at": {
                 "atMobiles": [
                     "15810186753",
                     "15311449173"
                 ],
                 "isAtAll": False
             }
             }
    # data2 = {
    #     "msgtype": "link",
    #     "link": {
    #         "text": "机器人的使用文档，你值得拥有",
    #         "title": "钉钉机器人使用文档",
    #         "picUrl": "",
    #         "messageUrl": "https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq"
    #     }
    # }
    if _t == 'text':
        print('sending text...')
        json_data = json.dumps(data1)
    # elif _t == 'link':
    #     print('sending link...')
    #     json_data = json.dumps(data2)

    result = requests.post(
        url='https://oapi.dingtalk.com/robot/send?access_token=6c59df7784153aaa25094a5c0420d42dd65fe6ccdad83b4a2809ad9a444f7e82',
        data=json_data, headers=headers)
    print(result)


target_time = time.mktime(time.strptime("2020-12-31 15:57:00", "%Y-%m-%d %H:%M:%S"))
while True:
    now = time.time()
    print(now-target_time)
    if now > target_time:
        ding_talk('text')
        break

# ding_talk('text')
# ding_talk('text')
