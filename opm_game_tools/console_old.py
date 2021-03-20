import openpyxl
import os
import webbrowser
import pyperclip
import requests


def change_dev_data():

    server = input('请输入服务器id:')
    user_id = input('请输入用户id(15位数字):')

    while True:
        print('\n请选择修改的数据类型：'
              '\n[1] 修改玩家资源'
              '\n[2] 添加卡牌'
              '\n[3] 添加道具'
              '\n[4] 添加所有装备'
              '\n[5] 修改关卡进度'
              '\n[6] 修改极限模拟战进度'
              '\n[11] 模拟抽卡'
              '\n[12] 模拟心愿单抽卡'
              '\n[13] 真实抽卡'
              '\n[14] 神秘扭蛋抽卡'
              '\n[0] 返回上一层'
              )
        cmd = input('\nCommand: ')

        if cmd == '0':
            break

        elif cmd == '1':
            resource_type = input('请输入资源类型(coin,diamond,guild_coin,hero_exp,hero_powder,friend)\n')
            num = input('请输入资源数量:')
            url = f'http://106.75.31.248:8010/admin/magic?uid={user_id}&p={resource_type},{num}&server_id={server}&action=asset/update'
            # print(url)
            response = requests.get(url)
            print(response.text)

        elif cmd == '2':
            hid = input('请输入英雄id,多个以逗号分隔:')
            count = 1
            quality = input('请输入英雄品质:')
            level = input('请输入等级:')

            heroids = hid.split(',')
            for heroid in heroids:
                url = f'http://106.75.31.248:8010/admin/magic?uid={user_id}&p={heroid}&c={count}&q={quality}&l={level}&server_id={server}&action=hero/create'
                response = requests.get(url)
                print(response.text)

        elif cmd == '3':
            pid = input('请输入道具id:')
            num = input('请输入道具数量:')
            url = f'http://106.75.31.248:8010/admin/magic?uid={user_id}&p={pid},{num}&server_id={server}&action=prop/update'
            response = requests.get(url)
            print(response.text)

        elif cmd == '4':
            url = f'http://106.75.31.248:8010/admin/magic?uid={user_id}&p=all&server_id={server}&action=equip/create'
            response = requests.get(url)
            print(response.text)

        elif cmd == '5':
            stage = input('请输入章节序号(章,节):')
            url = f'http://106.75.31.248:8010/admin/magic?uid={user_id}&p={stage}&server_id={server}&action=stage/changeRecord'
            response = requests.get(url)
            print(response.text)

        elif cmd == '6':
            level = input('请输入层数序号(类型,层数):')
            url = f'http://106.75.31.248:8010/admin/magic?uid={user_id}&p={level}&server_id={server}&action=extremeSimulation/changeRecord'
            response = requests.get(url)
            print(response.text)

        elif cmd == '11':
            browser = webbrowser.get('Chrome')
            url = 'http://106.75.31.248:8010/admin/magic?server_id=3&sid=2&c=1000&action=drawCard/simulate'
            browser.open(url)

        elif cmd == '12':
            browser = webbrowser.get('Chrome')
            url = 'http://106.75.31.248:8010/admin/magic?server_id=3&sid=2&c=1000&wishArm=1,18;2,20;3,21;4,23;5,32&wishPower=1,38;2,34;3,31;4,36;5,39&wishTech=1,45;2,8;3,12;4,24;5,44&wishFight=1,33;2,62;3,63;4,19;5,13&action=drawCard/simulate'
            browser.open(url)

        elif cmd == '13':
            browser = webbrowser.get('Chrome')
            url = 'http://106.75.31.248:8010/admin/magic?server_id=3&uid=844424930132040&sid=5&c=20&action=drawCard/user'
            browser.open(url)

        elif cmd == '14':
            browser = webbrowser.get('Chrome')
            url = 'http://106.75.31.248:8010/admin/magic?server_id=3&uid= 844424930132040&sid=3&c=20&r=49&action=newDrawCard/user'
            browser.open(url)

        else:
            print('输入的命令有误！请直接输入数字后回车！')

        input('\n执行完毕！\n输入回车继续！')

def main():
    browser = webbrowser.get('Chrome')
    os.system('clear')
    print(
        '*' * 50 + '\n' + '*' * 50 + '\n' + 'Welcome to One Punch Man Data Control Center!\n' + '*' * 50 + '\n' + '*' * 50 + '\n')

    while True:
        print('*' * 100)
        print('\n请选择命令(数字):'
              '\n[11] 发布Dev数据'
              '\n[12] 发布Dev服务器'
              '\n[13] 修改Dev数据'
              '\n[21] 发布Stage数据'
              '\n[31] Merge Release数据'
              '\n[32] 发布Release数据'
              '\n[33] 发布Review数据'
              '\n[41] 导出语言'
              '\n[0] Exit'
              )
              # '\n[34] 同步Release各服Configs数据'
              # '\n[1] 更新Common数据(执行update_specs)'
              # '\n[2] 更新单服数据(执行 update_specs server)'
              # '\n[3] 打开Spec—Excel的路径'

        cmd = input('\nCommand: ')

        if cmd == '0':
            # 退出
            print('\n(ㄏ￣▽￣)ㄏ Goodbye ㄟ(￣▽￣ㄟ)!\n')
            exit()

        # elif cmd == '1':
        #     # 更新common数据
        #     os.system('/Users/oas/Documents/work/github/opm_specs/tools/update_configs_specs.sh')

        # elif cmd == '2':
        #     # 更新单服数据
        #     servers = input('输入服务器列表(多服以逗号间隔)：').split(',')
        #     for i in servers:
        #         i = int(i)
        #         print('\nHandling Server : %d ....' % i)
        #         os.system('/Users/oas/Documents/work/github/opm_specs/tools/update_configs_specs.sh %d' % i)
        #         print('Server %d Done!\n' % i)

        # elif cmd == '3':
        #     os.system('open /Users/oas/Documents/work/github/opm_specs/specs/')

        elif cmd == '41':
            os.system('python3 /Users/oas/Documents/work/github/opm_specs/tools/convert_language.py')

        elif cmd == '11':
            # 发布Dev数据
            browser.open('http://106.75.31.248:7999/view/Develop-%E6%9B%B4%E6%96%B0%E4%BB%A3%E7%A0%81%E4%B8%8Espec'
                         '/job/opm-develop-spec-update/build?delay=0sec')
            pyperclip.copy('7805c2cdad465e24')

        elif cmd == '12':
            # 发布Dev服务器
            browser.open('http://106.75.31.248:7999/view/Develop-%E6%9B%B4%E6%96%B0%E4%BB%A3%E7%A0%81%E4%B8%8Espec'
                         '/job/opm-develop-server-update-new/build?delay=0sec')
            pyperclip.copy('7805c2cdad465e24')

        elif cmd == '13':
            # 修改Dev数据
            change_dev_data()

        elif cmd == '21':
            # 发布Stage数据
            browser.open('http://106.75.31.248:7999/view/Stage-%E6%9B%B4%E6%96%B0%E4%BB%A3%E7%A0%81%E4%B8%8Espec'
                         '/job/opm-stage-spec-update/build?delay=0sec')

        elif cmd == '31':
            # Merge线上数据
            browser.open('http://117.50.22.39/opm_v2/opm_specs/merge_requests/new')

        elif cmd == '32':
            # 发布线上数据
            browser.open('http://34.239.231.36:7999/job/mpsen-release-spec-update/build?delay=0sec')

        elif cmd == '33':
            # 发布Review数据
            browser.open('http://34.239.231.36:7999/job/mpsen-review-spec-update/build?delay=0sec')

        # elif cmd == '34':
        #     # 同步Release各服Configs数据
        #     os.system('python3 /Users/oas/Documents/work/github/opm_specs/tools/update_configs.py')

        else:
            print('输入的命令有误！请直接输入数字后回车！')

        input('\n执行完毕！\n输入回车继续！')
        print('*' * 100)


if __name__ == '__main__':
    main()
