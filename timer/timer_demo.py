# MMP, import顺序不一样居然都会报无限递归的错误！！！
# 这个脚本需要放到服务器上运行
import opm_tga.tga as tga
from ding_robot.robot_talk import ding_talk
import threading
import time


def daily_mission():
    s = tga.get_all_stats()
    ding_talk(s)


def timer_task():
    print(time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
    daily_mission()

    global timer
    timer= threading.Timer(86400, timer_task)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(2, timer_task)
    timer.start()


# target_time = time.mktime(time.strptime("2020-12-31 15:57:00", "%Y-%m-%d %H:%M:%S"))
# while True:
#     now = time.time()
#     print(now-target_time)
#     if now > target_time:
#         ding_talk('text')
#         break
