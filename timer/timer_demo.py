import threading
import time

curTime = time.strftime("%Y-%M-%D", time.localtime())  # 记录当前时间
execF = False


def exec_task():
    # 具体任务执行内容
    print("execTask executed!")


def timer_task():
    global execF
    global curTime
    if execF is False:
        exec_task()  # 判断任务是否执行过，没有执行就执行
        execF = True
    else:  # 任务执行过，判断时间是否新的一天。如果是就执行任务
        desTime = time.strftime("%Y-%M-%D", time.localtime())
        if desTime > curTime:
            execF = False  # 任务执行执行置值为
            curTime = desTime

    timer_1 = threading.Timer(5, timer_task)
    timer_1.start()


if __name__ == "__main__":
    timer = threading.Timer(5, timer_task)
    timer.start()
