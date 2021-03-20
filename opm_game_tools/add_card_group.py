# 过时脚本
# 用于批量添加角色

import os
import pyperclip
import requests
import random


def get_rand_hero():
    hero_list = [1,2,8,10,11,12,13,18,19,20,21,23,24,25,26,27,31,32,34,35,36,38,39,41,42,43,44,45,46,49,51,60,61,63,83,84,85,86,87,88,89]
    return random.choice(hero_list)

def get_rand_quality():
    return random.randint(14,15)

def get_rand_level(quality):
    if quality <= 5:
        return random.randint(80,100)
    else:
        return random.randint(20 * quality - 19, 20 * quality)

def change_dev_data(server,user_id):
    
    heroids = []
    quality = get_rand_quality()

    for i in range(0,10):
        heroid = get_rand_hero()
        while heroid in heroids:
            heroid = get_rand_hero()

        heroids.append(heroid)
        level = get_rand_level(quality)

        url = f'http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid={user_id}&p={heroid}&c=1&q={quality}&l={level}&server_id={server}&action=hero/create'
        # print(url)
        response = requests.get(url)
        print(response.text)

        url = f'http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid={user_id}&p=5,21&server_id={server}&action=stage/changeRecord'
        response = requests.get(url)
        print(response.text)


    print('*' * 20)

def main():
  
    os.system('clear')
    print('*' * 50 + '\n' + '*' * 50 + '\n' + 'Welcome to Add Card Group !\n' + '*' * 50 + '\n' + '*' * 50 + '\n')

    server_list = [2]
    user_id_list = [562949953421511]
    for x in range(0,len(server_list)):
        change_dev_data(server_list[x],user_id_list[x])

    print('*' * 50 + '\n' + '*' * 50 + '\n' + '执行完毕！ !\n' + '*' * 50 + '\n' + '*' * 50 + '\n')


if __name__ == '__main__':
    main()
