# -*- coding: utf-8 -*-
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 引用自定义函数
os.chdir('D:/user/Documents/00code/spyder_exam/项目13社会财富分配问题模拟')
# os.chdir('/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟')
import PJ13_function as pjSelf


pathPj13 = os.path.abspath('.')
person_n = [x for x in range(1, 101)]
print('导入模块完成')

# %%设置输出的地址
exportQ1NoSort = "%s/输出/问题1_不允许借贷—不排序" % pathPj13
exportQ1Sort = "%s/输出/问题1_不允许借贷—排序" % pathPj13
exportQ2Sort = "%s/输出/问题2_允许借贷—排序" % pathPj13
exportQ2SortNeg = "%s/输出/问题2_允许借贷—排序—负债" % pathPj13
exportQ3SortEff = "%s/输出/问题3_不允许借贷—排序—努力" % pathPj13
exportQ4SortQ4 = "%s/输出/问题4_自建模型" % pathPj13
print('设置系统量完成')

# %% 问题1
# 设定初始参数：游戏玩家100人，起始资金100元
fortuneQ1 = pd.DataFrame([100 for i in range(100)], index=person_n)
fortuneQ1.index.name = 'id'
print('初始值设定完成')
# 开始循环
startTime = time.time()
for i in range(1, 17001):
    fortuneQ1[i] = pjSelf.processQ1(fortuneQ1, i)
resultQ1 = fortuneQ1.T
endTime = time.time()
print('问题一总共运行%i秒' % (endTime - startTime))

print(resultQ1.tail())
del i, startTime, endTime
# %%问题1 绘制柱状图
resultQ1Max = resultQ1.iloc[-1].max() + 20

os.chdir(exportQ1NoSort)

pjSelf.Pic1(resultQ1, 0, 100, 10, resultQ1Max)
pjSelf.Pic1(resultQ1, 100, 1000, 100, resultQ1Max)
pjSelf.Pic1(resultQ1, 1000, 17001, 400, resultQ1Max)

print("'问题1:不允许借贷—不排序'输出完成")

os.chdir(exportQ1Sort)

pjSelf.Pic2(resultQ1, 0, 100, 10, resultQ1Max, 0)
pjSelf.Pic2(resultQ1, 100, 1000, 100, resultQ1Max, 0)
pjSelf.Pic2(resultQ1, 1000, 17001, 400, resultQ1Max, 0)

print("'问题2:不允许借贷—排序'输出完成")

# %% 问题1 结论
resultFinsh = pd.DataFrame({'assets': resultQ1.iloc[-1]}).sort_values(by='assets', ascending=False).reset_index()

resultFinsh['assets_pre'] = resultFinsh['assets'] / resultFinsh['assets'].sum() * 100
resultFinsh['assets_cumsum'] = resultFinsh['assets_pre'].cumsum()
resultFinsh.head(20)
print('最富有的人财富值为%i元，相比于初始财富，翻了%.2f倍' % (resultFinsh['assets'][1], resultFinsh['assets'][1] / 100))
print('10%%的人掌握着%.02f%%的财富' % (resultFinsh['assets_cumsum'][9]))
print('%i%%的人财富缩水至100元以下' % len(resultFinsh[resultFinsh['assets'] < 100]))

# %%
del exportQ1NoSort, exportQ1Sort, resultQ1Max, fortuneQ1, resultFinsh

####################################################
# %% 问题2.1

# 设定初始参数：游戏玩家100人，起始资金100元
fortuneQ2 = pd.DataFrame([100 for i in range(100)], index=person_n)
fortuneQ2.index.name = 'id'
print('初始值设定完成')
# 开始循环
startTime = time.time()
for i in range(1, 17001):
    fortuneQ2[i] = pjSelf.processQ2(fortuneQ2, i)
resultQ2 = fortuneQ2.T
endTime = time.time()
print('问题2.1总共运行%i秒' % (endTime - startTime))

print(resultQ2.tail())
del i, startTime, endTime

# %% 问题2.1 绘制柱状图
resultQ2Max = resultQ2.iloc[-1].max() + 20
resultQ2Min = resultQ2.iloc[-1].min() - 5

os.chdir(exportQ2Sort)

pjSelf.Pic2(resultQ2, 0, 100, 10, resultQ2Max, resultQ2Min)
pjSelf.Pic2(resultQ2, 100, 1000, 100, resultQ2Max, resultQ2Min)
pjSelf.Pic2(resultQ2, 1000, 17001, 400, resultQ2Max, resultQ2Min)

print("'问题2:允许借贷—不排序'输出完成")

# %% 问题2.1 结论
resultFinsh = pd.DataFrame({'assets': resultQ2.iloc[-1]}).sort_values(by='assets', ascending=False).reset_index()

resultFinsh['assets_pre'] = resultFinsh['assets'] / resultFinsh['assets'].sum() * 100
resultFinsh['assets_cumsum'] = resultFinsh['assets_pre'].cumsum()
resultFinsh.head(20)
print('问题2.1 结论')
print('最富有的人财富值为%i元，相比于初始财富，翻了%.2f倍' % (resultFinsh['assets'][1], resultFinsh['assets'][1] / 100))
print('10%%的人掌握着%.02f%%的财富' % (resultFinsh['assets_cumsum'][9]))
print('20%%的人掌握着%.02f%%的财富' % (resultFinsh['assets_cumsum'][19]))
print('%i%%的人财富缩水至100元以下' % len(resultFinsh[resultFinsh['assets'] < 100]))

# %% 问题2.1 标准差的情况，绘图来表示

resultSt = resultQ2.std(axis=1)
plt.figure(figsize=(10, 6))
resultSt.plot(color='red', alpha=0.6, grid=True)
plt.xlabel('round')
plt.ylabel('std')
plt.title('QUESTION2.1 STD-Round')

# %%
del resultSt, resultFinsh, resultQ2
####################################################
# %% 问题2.2
# 玩家从18岁开始，在经过17年后为35岁，这个期间共进行游戏6200次左右，则此刻查看财富情况，将财富值为负的标记成“破产

fortuneQ2['color'] = 'gray'
fortuneQ2['color'][fortuneQ2[6200] < 0] = 'red'

resultQ2IDList = fortuneQ2[fortuneQ2[6200] < 0].index.tolist()

print("35岁财富值为负的玩家id为：\n", resultQ2IDList)
# %% 问题2.2 绘制柱状图

os.chdir(exportQ2SortNeg)

pjSelf.Pic3(fortuneQ2, 1000, 17001, 400, resultQ2Max, resultQ2Min)
print("'问题2:允许借贷—排序—负债'输出完成")
# %% 问题2.2 最穷的人与最富有的人的财产变化
resultQ22 = fortuneQ2.sort_values(by=17000)
del resultQ22['color']
resultQ22 = pd.DataFrame({'richman': resultQ22.iloc[-1],
                          'poolman': resultQ22.iloc[0]})
resultQ22.plot(kind='line', figsize=(10, 6), grid=True)
# %%
del resultQ22, resultQ2Max, resultQ2Min
####################################################
# %% 问题3 努力的人生
# person_p(频率参数)在函数文件中创建
person_c = ['gray' for i in range(100)]
for i in [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]:
    person_c[i - 1] = 'red'

# %%
# 设定初始参数：游戏玩家100人，起始资金100元
fortuneQ3 = pd.DataFrame([100 for i in range(100)], index=person_n)
fortuneQ3.index.name = 'id'
print('初始值设定完成')

# 开始循环
startTime = time.time()
for i in range(1, 17001):
    fortuneQ3[i] = pjSelf.processQ4(fortuneQ3, i)
endTime = time.time()
print('问题3总共运行%i秒' % (endTime - startTime))

print(fortuneQ3.tail())
del i, startTime, endTime
fortuneQ3['color'] = person_c
# %% 问题3 绘制柱状图
resultQ3Max = fortuneQ3[17000].max() + 20
resultQ3Min = fortuneQ3[17000].min() - 5

os.chdir(exportQ3SortEff)

pjSelf.Pic3(fortuneQ3, 0, 100, 10, resultQ3Max, resultQ3Min)
pjSelf.Pic3(fortuneQ3, 100, 1000, 100, resultQ3Max, resultQ3Min)
pjSelf.Pic3(fortuneQ3, 1000, 17001, 400, resultQ3Max, resultQ3Min)

print("'问题3:不允许借贷—排序—努力'输出完成")
del resultQ3Max, resultQ3Min, person_c

####################################################
# %% 问题4 自建模型
# 设定初始参数：游戏玩家100人，起始资金100元,国家资金1000元
person_g = person_n.copy()
del person_g[15:20]

# 设定35岁前努力与一直努力的获得概率
person_p41 = [0.894 / 85 for i in range(95)]
for i in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
    person_p41[i - 1] = 0.0106

person_p42 = [0.947 / 90 for i in range(95)]
for i in [11, 12, 13, 14, 15]:
    person_p42[i - 1] = 0.0106

person_c = ['gray' for i in range(100)]
# 偷税者
for i in [1, 2, 3, 4, 5]:
    person_c[i - 1] = 'red'
# 17-35岁努力 ：蓝色表示
for i in [6, 7, 8, 9, 10]:
    person_c[i - 1] = 'blue'
# 一直努力 ：绿色表示
for i in [11, 12, 13, 14, 15]:
    person_c[i - 1] = 'green'
# 公务员 : 橙色表示
for i in [16, 17, 18, 19, 20]:
    person_c[i - 1] = 'orange'

# %%开始循环

fortuneQ4 = pd.DataFrame([100 for i in range(100)], index=person_n)
fortuneQ4.index.name = 'id'
print('初始值设定完成')
fortuneQ40 = 1000

startTime = time.time()
for i in range(1, 6201):
    fortuneQ4[i], fortuneQ41 = pjSelf.processQ5(fortuneQ4, i, person_p41)
    fortuneQ40 = fortuneQ40 - 8.15 + fortuneQ41
    print(i, '::', fortuneQ4[i].sum() + fortuneQ40)
endTime = time.time()
print('问题4总共运行%i秒' % (endTime - startTime))

# fortuneQ42 = fortuneQ4.copy()

for i in range(6201, 17001):
    fortuneQ4[i], fortuneQ41 = pjSelf.processQ5(fortuneQ4, i, person_p42)
    fortuneQ40 = fortuneQ40 - 8.15 + fortuneQ41
    print(i, '::', fortuneQ4[i].sum() + fortuneQ40)

resultQ4 = fortuneQ4.T

endTime = time.time()
print('问题4总共运行%i秒' % (endTime - startTime))

print(resultQ4.tail())

print('公务员工资:如果公务员的工资为1.9,则公务员必定为最富有的,小于1.6时,公务员必定是最穷的')
print('公务员工资:公务员工资在1.6-1.7之间时,公务员资产在100之间')
print('公务员工资:最终确定为1.63')
print('税率:在税率为6%时,国家在600轮内资金增加1500,资金大于100就可以算"富豪"了')
print('税率:在税率为5%时,国家在600轮内资金亏300')
print('税率:最终确定为5.1%,就当是通货紧缩')
print('最终国家资金增长%.2f元' % (fortuneQ40 - 1000))

fortuneQ4['color'] = person_c
# %%
del i, startTime, endTime, person_p41, person_p42, resultQ4, person_c, person_g, fortuneQ41

# %%
os.chdir(exportQ4SortQ4)

resultQ4Max = fortuneQ4[17000].max() + 20
# resultQ4Min = fortuneQ4[17000].min() - 5


pjSelf.Pic3(fortuneQ4, 0, 100, 10, resultQ4Max, 0)
pjSelf.Pic3(fortuneQ4, 100, 1000, 100, resultQ4Max, 0)
pjSelf.Pic3(fortuneQ4, 1000, 17001, 400, resultQ4Max, 0)

print("'问题4_自建模型'输出完成")
del resultQ4Max
