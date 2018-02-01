# -*- coding:utf-8 -*-
from TimeToName import time_name
import time
import pandas as pd

start = time.clock()    # 记录程序开始的时间
name = time_name(2017, 12, 16)  # 调用time_name程序

Path = r'D:\Python Study\利用Python读取EMS数据\01 20171217EMS数据'

txtFile = '有功无功.txt'    # 这个txt文件是所要读取的厂站信息
txt = open(txtFile, encoding='UTF-8')   # 打开这个txt文件，采用的编码形式是UTF-8
nameOfPower1 = txt.read()   # read方法表示读取文件里的所有内容
nameOfPower1 = nameOfPower1.splitlines()    # splitlines方法表示根据\n来分行，并且去掉\n
nameOfPower = list(set(nameOfPower1))       # set是集合方法，是一个无序无重复值的集合，用来去掉重复值；set后返回的是集合
nameOfPower.sort(key=nameOfPower1.index)    # sort方法是排序，key表示按照何种方法排序
ZHI1 = pd.DataFrame(index=nameOfPower)      # DataFrame是建立一个类似矩阵的东西，index表示其索引，内容为空
txt.close()     # 关闭所打开的txt文件

range_end = 288     # 需要读取的时间点数，一天288个点

print(0)
file = Path + '\EMS_15M_' + name[0] + '.dat'
EMS1 = open(file, 'r')
line = EMS1.read()
line = line.splitlines()
line1 = line[2:-1]  # 去掉前两行和最后一行

line2 = list(map(lambda w: w.split(','), line1))
temp = pd.DataFrame(line2)
CZ = temp[0] + ',' + temp[1] + ',' + temp[2]
ZHI = temp[3]
ZHI = list(map(float, ZHI))


y = pd.DataFrame(ZHI, index=CZ, columns=[name[0]])  # 创建一个DataFrame
y = y.loc[nameOfPower]  # loc方法表示索引按照nameOfPower来取数

dIndex = y.index.duplicated()   # duplicated方法表示找出重复值，返回true或者false
y = y[~dIndex]  # ~表示取反
ZHI1 = ZHI1.join(y, how='left')     # join方法是将y按照索引值加入到ZHI1之中，加入的方式left表示以ZHI1的索引为准

for i in range(1, range_end):
    print(i)
    file = Path + '\EMS_15M_' + name[i] + '.dat'    # 依次打开文件
    EMS1 = open(file, 'r')
    line = EMS1.read()
    line = line.splitlines()
    line1 = line[2:-1]      # 去掉前两行和最后一行

    line2 = list(map(lambda w: w.split(','), line1))
    temp = pd.DataFrame(line2)
    CZ = temp[0] + ',' + temp[1] + ',' + temp[2]
    ZHI = temp[3]
    ZHI = list(map(float, ZHI))

    y = pd.DataFrame(ZHI, index=CZ, columns=[name[i]])
    y = y.loc[nameOfPower]
    dIndex = y.index.duplicated()
    y = y[~dIndex]
    ZHI1 = ZHI1.join(y, how='left')
    EMS1.close()

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
