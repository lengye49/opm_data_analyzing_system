import os
import time
import datetime


# 判断文件夹是否存在
dir_path = ''
os.path.exists(dir_path)


file_path = ''
# 判断文件或文件夹是否存在
os.path.exists(file_path)
# 只判断是否存在文件
os.path.isfile(file_path)


# 获取文件大小,KB
def get_file_size(_path):
    file_size = os.path.getsize(_path)
    file_size = file_size/1024.0
    return round(file_size, 2)


# 时间戳转换为时间
def time_stamp_to_time(time_stamp):
    time_struct = time.localtime(time_stamp)
    return time.strftime('%Y-%M-%D %H:%M:%S',time_struct)


# 获取文件访问时间
def get_file_access_time(_path):
    t = os.path.getatime(_path)
    return time_stamp_to_time(t)


# 获取文件创建时间
def get_file_create_time(_path):
    t = os.path.getctime(_path)
    return time_stamp_to_time(t)


# 获取文件修改时间
def get_file_modify_time(_path):
    t = os.path.getmtime(_path)
    return time_stamp_to_time(t)
