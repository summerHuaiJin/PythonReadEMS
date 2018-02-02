# -*- coding:utf-8 -*-
import time
import pandas as pd
import numpy as np


def time_name(year, month, day, days=1, minutes=5):
    """ 这是一个将年月日时分转化为一串字符的程序
     例如，2017年12月16日1点05分，将表示成201712160105
     引用格式为t_name = time_name(year, month, day, days, minutes=5)
     其中，倒数第二个参数days表示持续的天数，可不输入，默认值为1
     最后的参数minutes表示间隔的分钟，可不输入，默认为5
     输出为t_name，类型为list"""
    year = str(year).zfill(4)  # zfill方法表示对字符串补位，高位补零
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    first_time = year + '-' + month + '-' + day + ' 00:00:00'  # 字符串可以直接用加法运算
    # 转换成时间数组
    time_array = time.strptime(first_time, "%Y-%m-%d %H:%M:%S")  # 时间数组元素依次为年、月、日……秒
    # 转换成时间戳
    timestamp = time.mktime(time_array)  # 时间戳是以秒为单位的一串数字

    # numpy.arange方法跟range差不多，可以处理浮点数；
    timestamp_list = list(np.arange(timestamp, timestamp + days * 24 * 60 * 60, 60 * minutes))

    # map(A, B)表示将A方法作用在列表B中的每一个元素，返回的是map类型，用list转化为列表
    time_array = list(map(time.localtime, timestamp_list))
    time_array1 = list(map(lambda x: str(x[0]).zfill(4) + str(x[1]).zfill(2) + str(x[2]).zfill(2), time_array))
    time_array2 = list(map(lambda x: str(x[3]).zfill(2) + str(x[4]).zfill(2), time_array))
    t_name = list(map(lambda x, y: x + y, time_array1, time_array2))

    return t_name


def read_input(txt_file):
    """读取input文件
    引用方式为name_of_input = read_input(txt_file)
    输入txt_file是input文件的名字（包含完整路径）
    输出name_of_input将input文件转化为list，同时去除重复值"""

    txt = open(txt_file, encoding='UTF-8')   # 打开这个txt文件，采用的编码形式是UTF-8
    name_of_power1 = txt.read()   # read方法表示读取文件里的所有内容
    name_of_power1 = name_of_power1.splitlines()    # splitlines方法表示根据\n来分行，并且去掉\n
    name_of_input = list(set(name_of_power1))       # set是集合方法，是一个无序无重复值的集合，用来去掉重复值；set后返回的是集合
    name_of_input.sort(key=name_of_power1.index)    # sort方法是排序，key表示按照何种方法排序
    txt.close()     # 关闭所打开的txt文件
    return name_of_input


def read_dat(file, name, zhi1):
    """读取dat文件的循环体
    引用格式为zhi1 = read_dat(file, name, zhi1)
    输入file为dat文件名，包括完整路径
    输入name为时间名，如201712160130
    输入和输出zhi1为DataFrame数据类型，index为input文件中的元素，columns为时间
    引用本函数前应先初始化zhi1"""

    ems1 = open(file, 'r')
    line = ems1.read()
    line = line.splitlines()
    line1 = line[2:-1]  # 去掉前两行和最后一行

    line2 = list(map(lambda w: w.split(','), line1))    # map(A, B)方法表示将A方法作用于列表B中的每一个元素
    temp = pd.DataFrame(line2)
    cz = temp[0] + ',' + temp[1] + ',' + temp[2]
    zhi = temp[3]
    zhi = list(map(float, zhi))  # float方法只能对单个值使用，利用map方法作用于zhi的每一个元素

    y = pd.DataFrame(zhi, index=cz, columns=[name])  # 创建一个DataFrame
    y = y.loc[nameOfPower]  # loc方法表示索引按照nameOfPower来取数

    d_index = y.index.duplicated()  # duplicated方法表示找出重复值，返回true或者false
    y = y[~d_index]  # ~表示取反
    zhi1 = zhi1.join(y, how='left')  # join方法是将y按照索引值加入到ZHI1之中，加入的方式left表示以ZHI1的索引为准
    ems1.close()
    return zhi1


"""以下为主程序"""

start = time.clock()    # 记录程序开始的时间
Name = time_name(2017, 12, 16, 1, 5)  # 调用time_name程序
Path = r'D:\Python Study\利用Python读取EMS数据\01 20171217EMS数据'
nameOfPower = read_input('有功无功.txt')

ZHI1 = pd.DataFrame(index=nameOfPower)      # DataFrame是建立一个类似矩阵的东西，index表示其索引，内容为空

range_end = 288     # 需要读取的时间点数，一天288个点

for i in range(0, range_end):
    print(i)
    File = Path + '\EMS_15M_' + Name[i] + '.dat'
    ZHI1 = read_dat(File, Name[i], ZHI1)

gao = ZHI1.loc[ZHI1.index.str.contains('高端有功$')]    # DataFrame.index.str.contains()可以处理正则表达式
zhong = ZHI1.loc[ZHI1.index.str.contains('中端有功$')]
di = ZHI1.loc[ZHI1.index.str.contains('低端有功$')]

gaoWu = ZHI1.loc[ZHI1.index.str.contains('高端无功$')]
zhongWu = ZHI1.loc[ZHI1.index.str.contains('中端无功$')]
diWu = ZHI1.loc[ZHI1.index.str.contains('低端无功$')]
elapsed = (time.clock() - start)
print("Time used:", elapsed)

mid = time.clock()
writer = pd.ExcelWriter('try.xlsx')

gao.to_excel(writer, '高端有功')
elapsed = (time.clock() - mid)
print("写入高端有功所需时间:", elapsed)

mid = time.clock()
zhong.to_excel(writer, '中端有功')
elapsed = (time.clock() - mid)
print("写入中端有功所需时间:", elapsed)

mid = time.clock()
di.to_excel(writer, '低端有功')
elapsed = (time.clock() - mid)
print("写入低端有功所需时间:", elapsed)

mid = time.clock()
gaoWu.to_excel(writer, '高端无功')
elapsed = (time.clock() - mid)
print("写入高端无功所需时间:", elapsed)

mid = time.clock()
zhongWu.to_excel(writer, '中端无功')
elapsed = (time.clock() - mid)
print("写入中端无功所需时间:", elapsed)

mid = time.clock()
diWu.to_excel(writer, '低端无功')
elapsed = (time.clock() - mid)
print("写入低端无功所需时间:", elapsed)

mid = time.clock()
ZHI1.to_excel(writer, '总')
elapsed = (time.clock() - mid)
print("写入所有的有功无功所需时间:", elapsed)

mid = time.clock()
writer.save()

elapsed = (time.clock() - mid)
print("存储Excel所用时间:", elapsed)
elapsed = (time.clock() - start)
print('程序所用时间：', elapsed)
