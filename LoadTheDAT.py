# -*- coding:utf-8 -*-
from TimeToName import time_name
import time
import pandas as pd

name = time_name(2017, 12, 16)
CZ = []         # 厂站
line2 = []
WLL = []  # 物理量（即电压、电流、有功等）
ZHI = []  # 值
Path = r'D:\Python Study\利用Python读取EMS数据\01 20171217EMS数据'

start = time.clock()
range_end = 10

print(0)
file = Path + '\EMS_15M_' + name[0] + '.dat'
EMS1 = open(file, 'r')
line = EMS1.read()
line = line.splitlines()
line1 = line[2:-1]  # 去掉前两行和最后一行

for x in line1:
    line2.append(x.split(','))  # append方法表示从列表最后新增元素
    CZ.append(line2[-1][1] + ',' + line2[-1][2])  # 厂站位于第二列，Python计数从0开始，物理量位于第三列
    ZHI.append(float(line2[-1][-1]))  # 值在最后一列
CZ1 = CZ
ZHI1 = pd.DataFrame(ZHI, index=CZ, columns=[name[0]])
print(ZHI1)

for i in range(1, range_end):
    print(i)
    file = Path + '\EMS_15M_' + name[i] + '.dat'
    EMS1 = open(file, 'r')
    line = EMS1.read()
    line = line.splitlines()
    line1 = line[2:-1]      # 去掉前两行和最后一行
    line2 = []

    CZ = []
    ZHI = []
    for x in line1:
        line2.append(x.split(','))  # append方法表示从列表最后新增元素
        CZ.append(line2[-1][1] + ',' + line2[-1][2])         # 厂站位于第二列，Python计数从0开始，物理量位于第三列
        ZHI.append(float(line2[-1][-1]))            # 值在最后一列
    ZHI1[name[i]] = ZHI
    EMS1.close()
print(ZHI1)

gao = ZHI1.loc[ZHI1.index.str.contains('高端有功$')]
zhong = ZHI1.loc[ZHI1.index.str.contains('中端有功$')]
di = ZHI1.loc[ZHI1.index.str.contains('低端有功$')]
elapsed = (time.clock() - start)
print("Time used:", elapsed)

mid = time.clock()
writer = pd.ExcelWriter('try.xlsx')

gao.to_excel(writer, '高端有功')
elapsed = (time.clock() - mid)
print("写入高端所需时间:", elapsed)

mid = time.clock()
zhong.to_excel(writer, '中端有功')
elapsed = (time.clock() - mid)
print("写入中端所需时间:", elapsed)

mid = time.clock()
di.to_excel(writer, '低端有功')
elapsed = (time.clock() - mid)
print("写入低端所需时间:", elapsed)

writer.save()

elapsed = (time.clock() - start)
print("Time used:", elapsed)
