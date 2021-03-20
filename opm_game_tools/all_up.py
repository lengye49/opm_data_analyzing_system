import random
import requests
import os
import ast

def get_rand_hero():
    hero_list = [1,2,8,10,11,12,13,18,19,20,21,23,24,25,26,27,31,32,34,35,36,38,39,41,42,43,44,45,46,49,51,60,61,63,83,84,85,86,87,88,89,93]
    return hero_list

def get_rand_quality():
    hero_quality = [13,15]
    return random.choice(hero_quality)

def get_rand_level(quality):
    if quality <= 5:
        return random.randint(1,100)
    else:
        return random.randint(20 * quality - 19, 20 * quality)

def get_talent_level(hero_id):
    if hero_id in [61, 60, 62, 40, 84, 42]:
        talent_level = 40
    else:
        talent_level = 30
    return talent_level

def get_equip():
    equip_list = [3109,2109,1109,3209,2209,1209,3309,2309,1309,3409,2409,1409,3110,2110,1110,3210,2210,1210,3310,2310,1310,3410,2410,1410]
    return equip_list

def get_chapter_stage():
    chapter = 15
    stage = 20
    return chapter, stage

def change_dev_data(server,user_id,package):
    hero_list = get_rand_hero()
    quality = get_rand_quality()
    equip_id_list = get_equip()
    chapter_id, stage_id = get_chapter_stage()

    hero_count = len(hero_list)

    for i in range(1, hero_count):
        heroid = hero_list[i]
        level = get_rand_level(quality)
        talent = get_talent_level(heroid)

        url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&p={heroid}&c=1&q={quality}&l={level}&t={talent}&server_id={server}&action=hero/create'
        response = requests.get(url)
        print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&p={chapter_id},{stage_id}&server_id={server}&action=stage/changeRecord'
    response = requests.get(url)
    print(response.text)

    print(equip_id_list)
    for equip_id in equip_id_list:
        url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&p={equip_id}&server_id={server}&action=equip/create'
        response = requests.get(url)
        print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&p=all,5&server_id={server}&action=prop/update'
    response = requests.get(url)
    print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&p=diamond,10000000;coin,10000000000;hero_exp,100000000000;hero_powder,10000000000&server_id={server}&action=asset/update'
    response = requests.get(url)
    print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&lv=300&server_id={server}&action=hero/actionAcademyLevel'
    response = requests.get(url)
    print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&jobLv1=100&jobLv2=100&jobLv3=100&jobLv4=100&jobLv5=100&server_id={server}&action=hero/actionHeroJobLevels'
    response = requests.get(url)
    print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&lv=460&server_id={server}&action=hero/actionOverStep'
    response = requests.get(url)
    print(response.text)

    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={user_id}&isGm=1&server_id={server}&action=user/gmSetting'
    response = requests.get(url)
    print(response.text)

    print('*' * 10 + '\tDone!\t' + '*' * 10)

def main():
    os.system('clear')
    print('*' * 50 + '\n' + '*' * 50 + '\n' + 'Mission Start !\n' + '*' * 50 + '\n' + '*' * 50 + '\n')
    '''
    server_list = [2] 
    user_id_list = [562949953421630, 562949953421630]  
    package = 'dev'  # stage,dev
    '''
    server_list1 = input('server_id：')
    server_list = server_list1.split(',')
    user_id_list1 = input('uid (split by ,) ：')
    user_id_list = user_id_list1.split(',')
    package = input('stage,dev?')


    for x in range(0, len(user_id_list)):
        if len(server_list) == 1:
            change_dev_data(server_list[0], user_id_list[x], package)
        else:
            change_dev_data(server_list[x], user_id_list[x],package)
    print('*' * 50 + '\n' + '*' * 50 + '\n' + 'Done！ !\n' + '*' * 50 + '\n' + '*' * 50 + '\n')

if __name__ == '__main__':
    main()








