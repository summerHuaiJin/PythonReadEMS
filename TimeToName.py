# -*- coding:utf-8 -*-

""" 这是一个将年月日时分转化为一串字符的程序
 例如，2017年12月16日1点05分，将表示成201712160105
 输入为年月日，输出为name，类型为list，包含当日每隔五分钟的字符串，一共288个"""


def time_name(year, month, day):
    import time         # 导入time模块
    year = str(year).zfill(4)   # zfill方法表示对字符串补位，高位补零
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    hour = []       # 定义小时为空list
    minute = []     # 定义分钟为空list
    name = []       # 定义名称字符串为空list
    first_time = year + '-' + month + '-' + day + ' 00:00:00'   # 字符串可以直接用加法运算
    # 转换成时间数组
    timearray = time.strptime(first_time, "%Y-%m-%d %H:%M:%S")   # 时间数组元素依次为年、月、日……秒
    # 转换成时间戳
    timestamp = time.mktime(timearray)      # 时间戳是以秒为单位的一串数字

    hour.append(timearray[3])   # append方法表示从列表最后新增元素
    minute.append(timearray[4])
    hour_str = str(hour[-1]).zfill(2)   # zfill方法表示对字符串补位，高位补零
    minute_str = str(minute[-1]).zfill(2)
    name.append(year + month + day + hour_str + minute_str)

    for i in range(1, 288):
        timestamp = timestamp + 60 * 5
        timearray = time.localtime(timestamp)       # localtime方法表示将时间戳转化为时间数组形式
        hour.append(timearray[3])
        minute.append(timearray[4])
        hour_str = str(hour[-1]).zfill(2)
        minute_str = str(minute[-1]).zfill(2)
        name.append(year + month + day + hour_str + minute_str)
        # dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print(dt)
        # print(hour[-1])
        # print(minute[-1])
        # print('---------')
    return name
    # print(Name)
    # print(len(Name))
