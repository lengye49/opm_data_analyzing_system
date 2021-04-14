import os
import webbrowser
import pyperclip
import requests
import random
import pandas as pd


def show_all_commands():
    s = r"""全英雄
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421635&p=all&c=1&q=16&l=240&t=10&server_id=2&action=hero/create 
全道具
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=GYINBKQDMYT&p=all,999&server_id=4&action=prop/update
资源
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421424&p=diamond,10000000&server_id=2&action=asset/update
添加好友
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421361&action=friend/addFriends&server=2
调副本
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421390&p=7,11&server_id=2&action=stage/changeRecord
全装备
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=GYINBKQDMYZ&p=all&server_id=4&action=equip/create
改等级
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421345&p=level,2&server_id=2&action=user/updateUserBaseInfo
改玩家等级和经验
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421369&lv=7&exp=0&server_id=2&action=user/levelExpUpdate
强者之路重置
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421621&server_id=2&action=labyrinth/resetNormalRefreshTime
极限模拟战调整对应类型,层数
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421412&p=11,2&server_id=6&action=extremeSimulation/changeRecord
强者之路后退
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421412&server_id=5&num=10&action=labyrinth/back
强者之路前进
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421412&server_id=5&num=10&action=labyrinth/forward
竞技场重置
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421333&server_id=200&action=arena/resetDb
订阅
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?ouid=600685388249497&t=1599633614&server_id=2&action=subscribe/updateEndTime
查看战报
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?type=1&major=3&minor=4&action=combatReport/fetch
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=28167106617&type=1&major=3&minor=4&server_id=10&action=combatReport/fetch
修改GM
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421645&isGm=1&server_id=2&action=user/gmSetting
研究所等级
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421650&lv=300&server_id=2&action=hero/actionAcademyLevel
研究所职阶等级
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421650&jobLv1=100&jobLv2=100&jobLv3=100&jobLv4=100&jobLv5=100&server_id=2&action=hero/actionHeroJobLevels
修改新手引导
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=2814749767106561&guideId=50050&server_id=8&action=guide/updateRecord
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=2814749767106561&note=DrawCard&server_id=2&action=guide/rmTriggerRecord
战意等级
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=562949953421650&lv=310&server_id=2&action=hero/actionOverStep
限制器和机械核心
http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid=18577348462903345&heroId=36&mechanical=20&limiter=5&server_id=66&action=hero/actionUpgradeHeroInfo   
查看开服时间列表
http://center-mpsen.games.oasgames.com:8010/admin/getServerInitTime
    """
    print(s)


def get_rand_hero():
    hero_list = [1, 2, 8, 10, 11, 12, 13, 18, 19, 20, 21, 23, 24, 25, 26, 27, 31, 32, 34, 35, 36, 38, 39, 41, 42, 43,
                 44, 45, 46, 49, 51, 60, 61, 63, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                 101, 102, 103, 104, 105]
    return hero_list


def get_rand_quality():
    hero_quality = [13, 15]
    return random.choice(hero_quality)


def get_rand_level(quality):
    if quality <= 5:
        return random.randint(1, 100)
    else:
        return random.randint(20 * quality - 19, 20 * quality)


def get_talent_level(hero_id):
    if hero_id in [61, 60, 62, 40, 84, 42]:
        talent_level = 40
    else:
        talent_level = 30
    return talent_level


def get_equip():
    equip_list = [3109, 2109, 1109, 3209, 2209, 1209, 3309, 2309, 1309, 3409, 2409, 1409, 3110, 2110, 1110, 3210, 2210,
                  1210, 3310, 2310, 1310, 3410, 2410, 1410]
    return equip_list


def get_chapter_stage():
    chapter = 15
    stage = 20
    return chapter, stage


def random_change_data(server, user_id, package):
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


def random_all_up():
    server_list1 = input('server_id (split by ,) ：')
    server_list = server_list1.split(',')
    user_id_list1 = input('uid (split by ,) ：')
    user_id_list = user_id_list1.split(',')
    package = input('stage,dev?')

    for x in range(0, len(user_id_list)):
        if len(server_list) == 1:
            random_change_data(server_list[0], user_id_list[x], package)
        else:
            random_change_data(server_list[x], user_id_list[x], package)


def add_hero(hero_id, quality, lv, talent, package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&p={hero_id}&c=1&q={quality}' \
          f'&l={lv}&t={talent}&server_id={server_id}&action=hero/create'
    response = requests.get(url)
    print(df_hero.loc[hero_id, '_name'] + ':' + response.text)


def change_academy(lv, package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&lv={lv}&server_id={server_id}' \
          f'&action=hero/actionAcademyLevel'
    response = requests.get(url)
    print('修改研究所等级:' + str(lv) + ' ' + response.text)


def change_job(lv1, lv2, lv3, lv4, lv5, package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}' \
          f'&jobLv1={lv1}&jobLv2={lv2}&jobLv3={lv3}&jobLv4={lv4}&jobLv5={lv5}&server_id={server_id}' \
          f'&action=hero/actionHeroJobLevels'
    response = requests.get(url)
    print(
        '修改职阶等级:' + str(lv1) + ' ' + str(lv2) + ' ' + str(lv3) + ' ' + str(lv4) + ' ' + str(lv5) + ' ' + response.text)


def change_hero_connect(lv, package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&lv={lv}&server_id={server_id}' \
          f'&action=hero/actionOverStep'
    response = requests.get(url)
    print('修改战意连协等级:' + str(lv) + ' ' + response.text)


def add_all_equips(package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&p=all&server_id={server_id}' \
          f'&action=equip/create'
    response = requests.get(url)
    print('添加所有装备:' + response.text)


def change_assets(package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&server_id={server_id}' \
          f'&p=diamond,100000;coin,100000000;hero_exp,100000000000;hero_powder,99999999;droid_cost,9999999' \
          f'&action=asset/update'
    response = requests.get(url)
    print('添加资源:' + response.text)


def change_props(package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&p=all,9999&' \
          f'server_id={server_id}&action=prop/update'
    response = requests.get(url)
    print('添加所有道具:' + response.text)


def change_gm(package='dev'):
    url = f'http://center-mpsen-{package}.games.oasgames.com:8010/admin/magic?uid={uid}&isGm=1&' \
          f'server_id={server_id}&action=user/gmSetting'
    response = requests.get(url)
    print('修改GM:' + response.text)


def change_limiter_and_mechanical(hero_id, limiter_lv, mechanical_lv, package='dev'):
    url = f'http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid={uid}&server_id={server_id}&' \
          f'heroId={hero_id}&mechanical={mechanical_lv}&limiter={limiter_lv}&action=hero/actionUpgradeHeroInfo'
    response = requests.get(url)
    print('修改限制器和机械核心' + response.text)


def change_stage():
    url = f'http://center-mpsen-dev.games.oasgames.com:8010/admin/magic?uid={uid}&server_id={server_id}' \
          f'&p={15},{20}&action=stage/changeRecord'
    response = requests.get(url)
    print(response.text)


def generate_target_formation():
    global server_id
    server_id = int(input('server_id : '))
    global uid
    uid = int(input('uid : '))

    formation_str = input('formation : ')
    team_info = formation_str.split('$')

    connect_lv = 0
    academy = 0
    job = [0, 0, 0, 0, 0]

    summary = ''
    for member in team_info:

        hero_str = member.split('/')
        hero_pos = hero_str[0]

        hero_info = hero_str[1].split(';')
        # is_mercenary = int(hero_info[0])
        hero_id = int(hero_info[1])
        quality = int(hero_info[2])
        lv = int(hero_info[3])
        if lv > 240:
            connect_lv = lv
            lv = 240
        talent = int(hero_info[4])
        # enhance = int(hero_info[5])
        # 添加英雄

        # equip1 = hero_info[6]
        # equip2 = hero_info[7]
        # equip3 = hero_info[8]
        # equip4 = hero_info[9]

        academy_job = hero_info[10].split(',')
        academy = int(academy_job[0])
        _job = int(academy_job[1])
        _idx = df_hero.loc[hero_id, '_job'] - 30001
        job[_idx] = _job

        limiter = int(hero_info[11])
        mechanical_core = int(hero_info[12])

        summary += df_hero.loc[hero_id, '_name'] + ',位置：' + str(hero_pos) + ',战意：' + str(connect_lv) + \
                   ',研究所：' + str(academy) + ',职阶：' + str(_job) + ',限制器：' + str(limiter) + \
                   ',机械核心：' + str(mechanical_core) + '\n'

        add_hero(hero_id, quality, lv, talent)
        change_limiter_and_mechanical(hero_id, limiter, mechanical_core)

    # 修改研究所等级
    change_academy(academy)
    # 修改职阶等级
    change_job(job[0], job[1], job[2], job[3], job[4])
    # 添加所有装备
    add_all_equips()
    # 修改战意连协等级
    if connect_lv <= 0:
        pass
    else:
        change_hero_connect(connect_lv)
    # 修改资源
    change_assets()
    # 修改道具
    change_props()
    # 修改GM
    change_gm()
    # 临时将关卡调至15-20
    change_stage()
    print(summary)
    print('添加完成！')


df_hero = pd.read_excel('../opm_hero_property/design/hero_design.xlsx', header=0, index_col=0)
server_id = 0  # 66
uid = ''  # 18577348462903345


def main():
    # browser = webbrowser.get('Chrome')
    os.system('clear')
    print(
        '*' * 50 + '\n' + '*' * 50 + '\n' + '\t\t\t\t欢迎使用OPM集成脚本！\n'
        + '\t\t\t\t\t\t\t\t----Made by CnSky\n' + '*' * 50 + '\n' + '*' * 50 + '\n')
    print('测试账号：66, 18577348462903345')
    while True:
        print('*' * 50)
        print('\n请选择命令(数字):'
              '\n[1] 使用一键增强脚本'
              '\n[2] 生成目标阵容'
              '\n[0] 显示所有命令'
              )
        cmd = input('\nCommand: ')

        if cmd == '0':
            show_all_commands()
        if cmd == '1':
            random_all_up()
        if cmd == '2':
            generate_target_formation()


if __name__ == '__main__':
    main()
