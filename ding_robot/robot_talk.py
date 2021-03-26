#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author cn_sky
import requests
import json


def ding_talk(content=''):
    url = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=786b6e320aa4bc4889d5924c014b1b68d31f6d90e116d4597e347cbae655020c'
    content = 'python提示:\n' + content
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    data = {"msgtype": "text",
             "text": {
                 "content": content
             },
             "at": {
                 "atMobiles": [
                     "15810186753"
                 ],
                 "isAtAll": False
             }
             }

    # print(json.dumps(data))
    result = requests.post(url, data=json.dumps(data), headers=headers)
    print(result.text)

# ding_talk(text)
# ding_talk(t)
