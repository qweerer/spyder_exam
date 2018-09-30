# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
# 引用自定义函数
import PJ13_function as pjSelf

# os.chdir('D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出')
# os.chdir('.\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出')
person_n = [x for x in range(1, 101)]
print('导入模块完成')

# %%设置输出的地址
exportQ1NoSort = "/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟/输出/问题1:不允许借贷—不排序"
exportQ1Sort = "/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟/输出/问题1:不允许借贷—排序"
exportQ2NoSort = "/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟/输出/问题2:允许借贷—不排序"
exportQ2Sort = "/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟/输出/问题2:允许借贷—排序"
exportQ3NoSort = "/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟/输出/问题3:允许借贷-努力—不排序"
exportQ3Sort = "/home/qweerer/0code/spyder_exam/项目13社会财富分配问题模拟/输出/问题3:不允许借贷-努力—排序"
print('设置系统量完成')
# %%设置输出的地址
exportQ1NoSort = "D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出\\问题1:不允许借贷—不排序"
exportQ1Sort = "D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出\\问题1:不允许借贷—排序"
exportQ2NoSort = "D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出\\问题2:允许借贷—不排序"
exportQ2Sort = "D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出\\问题2:允许借贷—排序"
exportQ3NoSort = "D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出\\问题3:允许借贷-努力—不排序"
exportQ3Sort = "D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出\\问题3:不允许借贷-努力—排序"
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
# %%问题1绘制柱状图
resultQ1Max = resultQ1.iloc[-1].max() + 20

os.chdir(exportQ1NoSort)

pjSelf.Pic1(resultQ1, 0, 100, 10, resultQ1Max)
pjSelf.Pic1(resultQ1, 100, 1000, 100, resultQ1Max)
pjSelf.Pic1(resultQ1, 1000, 17001, 400, resultQ1Max)

print("'问题1:不允许借贷—不排序'输出完成")

os.chdir(exportQ1Sort)

pjSelf.Pic2(resultQ1, 0, 100, 10, resultQ1Max)
pjSelf.Pic2(resultQ1, 100, 1000, 100, resultQ1Max)
pjSelf.Pic2(resultQ1, 1000, 17001, 400, resultQ1Max)

print("'问题1:不允许借贷—不排序'输出完成")

# %% 问题1 结论
resultFinsh = pd.DataFrame({'assets': resultQ1.iloc[-1]}).sort_values(by='assets', ascending=False).reset_index()

resultFinsh['assets_pre'] = resultFinsh['assets'] / resultFinsh['assets'].sum() * 100
resultFinsh['assets_cumsum'] = resultFinsh['assets_pre'].cumsum()
resultFinsh.head(20)
print('10%%的人掌握着%.02f%%的财富' % (resultFinsh['assets_cumsum'][9]))
print('%i%%的人财富缩水至100元以下' % len(resultFinsh[resultFinsh['assets'] < 100]))

# %%
del exportQ1NoSort, exportQ1Sort, resultQ1Max, fortuneQ1, resultFinsh

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
print('问题一总共运行%i秒' % (endTime - startTime))

print(resultQ1.tail())
del i, startTime, endTime


# 一些结论

round_17000_2 = pd.DataFrame({'money': game2_result.iloc[17000]}).sort_values(by='money', ascending=False).reset_index()
round_17000_2['fortune_pre'] = round_17000_2['money'] / round_17000_2['money'].sum()
round_17000_2['fortune_cumsum'] = round_17000_2['fortune_pre'].cumsum()
round_17000_2.head()

# 最后一轮中，最富有的人财富值为458元，相比于初始财富，翻了4.58倍
# 10%的人掌握着33%的财富，20%的人掌握着59%的财富？
# 50%的人财富缩水至100元以下了？

# （3）游戏次数与财富分布的标准差的情况，绘图来表示

os.chdir('C:\\Users\\Hjx\\Desktop\\项目13社会财富分配问题模拟\\财富分配模型_允许借贷\\')


def graph3(data, start, end, length):
    for n in list(range(start, end, length)):
        datai = data.iloc[n].sort_values().reset_index()[n]
        plt.figure(figsize=(10, 6))
        plt.bar(datai.index, datai.values, color='gray', alpha=0.8, width=0.9)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.ylim((-200, 400))
        plt.xlim((-10, 110))
        plt.title('Round %d' % n)
        plt.xlabel('PlayerID')
        plt.ylabel('Fortune')
        plt.savefig('graph3_round_%d.png' % n, dpi=200)
# 创建绘图函数2


graph3(game2_result, 0, 100, 10)
graph3(game2_result, 100, 1000, 100)
graph3(game2_result, 1000, 17400, 400)

print('finished!')

# （4）游戏次数与财富分布的标准差的情况，绘图来表示

game2_st = game2_result.std(axis=1)
game2_st.plot(figsize=(12, 5), color='red', alpha=0.6, grid=True)
plt.show()

# 游戏早期前2000轮的标准差变动最为激烈；
# 而在6000-6500轮游戏后，标准差的变化趋于平缓，但仍在上升；
# 按照我们设定的游戏与人生的对应规则，这时玩家年龄为35岁

# （5）玩家从18岁开始，在经过17年后为35岁，这个期间共进行游戏6200次左右，则此刻查看财富情况，将财富值为负的标记成“破产
# 通过图表研究该类玩家在今后的游戏中能否成功“逆袭”（财富值从负到正为逆袭）、
# 这里绘制折线图

game2_round6200 = pd.DataFrame({'money': game2_result.iloc[6200].sort_values().reset_index()[6200],
                                'id': game2_result.iloc[6200].sort_values().reset_index()['id'],
                                'color': 'gray'})
game2_round6200['color'][game2_round6200['money'] < 0] = 'red'
id_pc = game2_round6200['id'][game2_round6200['money'] < 0].tolist()
print('财富值为负的玩家id为：\n', id_pc)
# 筛选数据
# 设置颜色参数

plt.figure(figsize=(10, 6))
plt.bar(game2_round6200.index, game2_round6200['money'], color=game2_round6200['color'], alpha=0.8, width=0.9)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.ylim((-200, 400))
plt.xlim((-10, 110))
plt.title('Round 6200')
plt.xlabel('PlayerID')
plt.ylabel('Fortune')
plt.show()
# 绘制柱状图

# 绘图分析

os.chdir('C:\\Users\\Hjx\\Desktop\\项目13社会财富分配问题模拟\\财富分配模型_允许借贷_负债玩家逆袭\\')


def graph4(data, start, end, length):
    for n in list(range(start, end, length)):
        datai = pd.DataFrame({'money': data.iloc[n], 'color': 'gray'})
        datai['color'].loc[id_pc] = 'red'
        datai = datai.sort_values(by='money').reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(datai.index, datai['money'], color=datai['color'], alpha=0.8, width=0.9)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.ylim((-200, 400))
        plt.xlim((-10, 110))
        plt.title('Round %d' % n)
        plt.xlabel('PlayerID')
        plt.ylabel('Fortune')
        plt.savefig('graph4_round_%d.png' % n, dpi=200)
# 创建绘图函数2


graph4(game2_result, 6200, 17000, 500)

print('finished!')

# 结论
# 以35岁为界，虽然破产以后，不足一半的概率回复到普通人的生活，但想要逆袭暴富，却是相当困难的










