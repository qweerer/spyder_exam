# -*- coding: utf-8 -*-
# %%
import os
import time

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pylab import mpl
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
# 导入图表绘制、图标展示模块
# output_file → 非notebook中创建绘图空间

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

os.chdir('D:/user/Documents/00code/spyder_exam/项目14婚恋配对实验/输出')
# os.chdir('/home/qweerer/0code/spyder_exam/项目14婚恋配对实验')

# pathPj14 = os.path.abspath('.')
print('导入模块完成')

#################################
# %%问题1
'''
1、样本数据处理
   ** 按照一定规则生成了1万男性+1万女性样本：
   ** 在配对实验中，这2万个样本具有各自不同的个人属性（财富、内涵、外貌），每项属性都有一个得分
   ** 财富值符合指数分布，内涵和颜值符合正态分布
   ** 三项的平均值都为60分，标准差都为15分
要求：
① 构建函数实现样本数据生成模型，函数参数之一为“样本数量”，并用该模型生成1万男性+1万女性数据样本
   ** 包括三个指标：财富、内涵、外貌
② 绘制柱状图来查看每个人的属性分值情况
提示：
① 正态分布：np.random.normal(loc=60, scale=15, size=n)
② 指数分布：np.random.exponential(scale=15, size=n) + 45
'''
# %%
dataM = pd.DataFrame({'fortune1': np.random.exponential(scale=15, size=100) + 45,
                      'character1': np.random.normal(loc=60, scale=15, size=100),
                      'appearances1': np.random.normal(loc=60, scale=15, size=100)},
                     index=['m%i' % i for i in range(1, 101)])
dataM['score1'] = (dataM['fortune1'] + dataM['character1'] + dataM['appearances1'])
dataM.index.name = 'MId'

dataF = pd.DataFrame({'fortune0': np.random.exponential(scale=15, size=100) + 45,
                      'character0': np.random.normal(loc=60, scale=15, size=100),
                      'appearances0': np.random.normal(loc=60, scale=15, size=100)},
                     index=['f%i' % i for i in range(1, 101)])
dataF['score0'] = (dataF['fortune0'] + dataF['character0'] + dataF['appearances0'])
dataF.index.name = 'FId'

# %%
figQ1 = plt.figure(figsize=(20, 6))
plt.subplots_adjust(hspace=0.3)

ax1 = figQ1.add_subplot(2, 1, 1)
dataM[['fortune1', 'character1', 'appearances1']].plot(kind='bar', stacked=True,
                                                       colormap='Blues',
                                                       edgecolor='black', alpha=0.7,
                                                       ax=ax1, rot=90)
plt.grid(color='grey', linestyle=':', linewidth=1, axis='y')
plt.legend(loc='upper right')

ax2 = figQ1.add_subplot(2, 1, 2)
dataF[['fortune0', 'character0', 'appearances0']].plot(kind='bar', stacked=True,
                                                       colormap='OrRd',
                                                       edgecolor='black', alpha=0.7,
                                                       ax=ax2, rot=90)
plt.legend(loc='upper right')
plt.grid(color='grey', linestyle=':', linewidth=1, axis='y')
plt.savefig('PJ14Q1.png', dpi=200)
#################################
# %%问题2.1 择偶策略，测试

dataQ2M = dataM.copy()
dataQ2F = dataF.copy()
matchSuccess = pd.DataFrame(columns=['m', 'f', 'round_n', 'strategyM', 'strategyF'])
# 构建空的数据集，用于存储匹配成功的数据

# %%
'''
2、生成99个男性、99个女性样本数据，分别针对三种策略构建算法函数
   ** 择偶策略1：门当户对，要求双方三项指标加和的总分接近，差值不超过20分；
   ** 择偶策略2：男才女貌，男性要求女性的外貌分比自己高出至少10分，女性要求男性的财富分比自己高出至少10分；
   ** 择偶策略3：志趣相投、适度引领，要求对方的内涵得分在比自己低10分~高10分的区间内，且外貌和财富两项与自己的得分差值都在5分以内
   ** 每一轮实验中，我们将三种策略随机平分给所有样本，这里则是三种策略分别33人
   ** 这里不同策略匹配结果可能重合，所以为了简化模型
   → 先进行策略1模拟，
   → 模拟完成后去掉该轮成功匹配的女性数据,再进行策略2模拟，
   → 模拟完成后去掉该轮成功匹配的女性数据,再进行策略3模拟
① 生成样本数据
② 给男性样本数据，随机分配策略选择 → 这里以男性为出发作为策略选择方
③ 尝试做第一轮匹配，记录成功的匹配对象，并筛选出失败的男女性进入下一轮匹配
④ 构建模型，并模拟1万男性+1万女性的配对实验
⑤ 通过数据分析，回答几个问题：
   ** 百分之多少的样本数据成功匹配到了对象？
   ** 采取不同择偶策略的匹配成功率分别是多少？
   ** 采取不同择偶策略的男性各项平均分是多少？
提示：
① 择偶策略评判标准：
   ** 若匹配成功，则该男性与被匹配女性在这一轮都算成功，并退出游戏
   ** 若匹配失败，则该男性与被匹配女性再则一轮都算失败，并进入下一轮
   ** 若同时多个男性选择了同一个女性，且满足成功配对要求，则综合评分高的男性算为匹配成功
② 构建空的数据集，用于存储匹配成功的数据
③ 每一轮匹配之后，删除成功匹配的数据之后，进入下一轮，这里删除数据用df.drop()
④ 这里建议用while去做迭代 → 当该轮没有任何配对成功，则停止实验
'''
# %%

dataQ2M['strategyM'] = np.random.choice([1, 2, 3], 100)
dataQ2F['strategyF'] = np.random.choice([1, 2, 3], 100)

dataQ2M['choiceM'] = np.random.choice(dataQ2F.index, len(dataQ2F))
dataQ2F['choiceF'] = np.random.choice(dataQ2M.index, len(dataQ2M))

# 复制男性样本数据，并做匹配选择
round1_match = pd.merge(dataQ2M, dataQ2F, left_on='choiceM', right_index=True).reset_index()

round1_match['score_dis'] = np.abs(round1_match['score0'] - round1_match['score1'])  # 计算综合评分差值
round1_match['cha_dis'] = np.abs(round1_match['character0'] - round1_match['character1'])  # 求出内涵得分差值
round1_match['for_dis'] = np.abs(round1_match['fortune0'] - round1_match['fortune1'])  # 求出财富得分差值
round1_match['app_dis'] = np.abs(round1_match['appearances0'] - round1_match['appearances1'])  # 求出外貌得分差值
# 合并数据
# %%
# 策略0: 一见钟情,男女两者互相喜欢
round1_s0 = round1_match[round1_match['MId'] == round1_match['choiceF']]
round1_s0 = pd.DataFrame({'m': round1_s0['MId'],
                          'f': round1_s0['choiceM'],
                          'round_n': 1,
                          'strategyM': round1_s0['strategyM'],
                          'strategyF': round1_s0['strategyF']})
# 因为一见钟情可能是任何形式的择偶,所以先删除
round1_match = round1_match.drop(round1_s0.index.tolist())

# 策略1：门当户对，要求双方三项指标加和的总分接近，差值不超过20分；
round1_s1 = round1_match[round1_match['strategyM'] == 1]  # 筛选男性为策略1的数据
round1_s1['mok'] = 0
round1_s1['fok'] = 0
# 判断男性的择偶是否符合
round1_s1['mok'][round1_s1['score_dis'] <= 20] = 1

round1_sc = pd.DataFrame(columns=round1_match.columns)
for i, j in round1_s1[round1_s1['mok'] == 1].groupby('strategyF'):
    if i == 1:
        j['fok'] = 1
        round1_sc = pd.concat([round1_sc, j])
    elif i == 2:
        j['fok'][j['fortune1'] - j['fortune0'] >= 10] = 1
        round1_sc = pd.concat([round1_sc, j])
    elif i == 3:
        j['fok'][(j['cha_dis'] < 10) &    # 内涵得分差在10分以内
                 (j['for_dis'] < 5) &     # 财富得分差在5分以内
                 (j['app_dis'] < 5)] = 1  # 外貌得分差在5分以内
        round1_sc = pd.concat([round1_sc, j])
round1_sc['OK'] = round1_sc['mok'] + round1_sc['fok']
round1_s1 = round1_sc[round1_sc['OK'] == 2]

# 策略2：男才女貌，男性要求女性的外貌分比自己高出至少10分
round1_s2 = round1_match[round1_match['strategyM'] == 2]
round1_s2['mok'] = 0
round1_s2['fok'] = 0
# 判断男性的择偶是否符合
round1_s2['mok'][(round1_s2['appearances0'] - round1_s2['appearances1']) >= 10] = 1  # 男性要求:女性颜值比男性高出至少10分

round1_sc = pd.DataFrame(columns=round1_match.columns)
for i, j in round1_s2[round1_s2['mok'] == 1].groupby('strategyF'):
    if i == 1:
        j['fok'][j['score_dis'] <= 20] = 1  # 女性要求:门当户对，要求双方三项指标加和的总分接近，差值不超过20分
        round1_sc = pd.concat([round1_sc, j])
    elif i == 2:
        j['fok'][j['fortune1'] - j['fortune0'] >= 10] = 1  # 女性要求:男性财富比女性高出至少10分
        round1_sc = pd.concat([round1_sc, j])
    elif i == 3:
        j['fok'][(j['cha_dis'] < 10) &  # 内涵得分差在10分以内
                 (j['for_dis'] < 5) &  # 财富得分差在5分以内
                 (j['app_dis'] < 5)] = 1  # 外貌得分差在5分以内
        round1_sc = pd.concat([round1_sc, j])
round1_sc['OK'] = round1_sc['mok'] + round1_sc['fok']
round1_s2 = round1_sc[round1_sc['OK'] == 2]

# 策略3：志趣相投、适度引领，要求对方的内涵得分在比自己低10分~高10分的区间内，且外貌和财富两项与自己的得分差值都在5分以内
round1_s3 = round1_match[round1_match['strategyM'] == 3]
round1_s3['mok'] = 0
round1_s3['fok'] = 0
# 判断男性的择偶是否符合
round1_s3['mok'][(round1_s3['cha_dis'] < 10) &  # 男性要求:内涵得分差在10分以内
                 (round1_s3['for_dis'] < 5) &  # 男性要求:财富得分差在5分以内
                 (round1_s3['app_dis'] < 5)] = 1  # 男性要求:女性颜值比男性高出至少10分

round1_sc = pd.DataFrame(columns=round1_match.columns)
for i, j in round1_s3[round1_s3['mok'] == 1].groupby('strategyF'):
    if i == 1:
        j['fok'][j['score_dis'] <= 20] = 1  # 女性要求:门当户对，要求双方三项指标加和的总分接近，差值不超过20分
        round1_sc = pd.concat([round1_sc, j])
    elif i == 2:
        j['fok'][j['fortune1'] - j['fortune0'] >= 10] = 1  # 女性要求:男性财富比女性高出至少10分
        round1_sc = pd.concat([round1_sc, j])
    elif i == 3:
        j['fok'] = 1  # 女性要求:与男性要求相同
        round1_sc = pd.concat([round1_sc, j])
round1_sc['OK'] = round1_sc['mok'] + round1_sc['fok']
round1_s3 = round1_sc[round1_sc['OK'] == 2]

# 对配对成功的进行合并,筛选
round1Succeed = pd.concat([round1_s1, round1_s2, round1_s3])
round1Succeed = round1Succeed.sort_values(by='score1', ascending=False)
round1Succeed = round1Succeed.drop_duplicates(subset=['choiceM'], keep='first')

round1Succeed = pd.DataFrame({'m': round1Succeed['MId'],
                              'f': round1Succeed['choiceM'],
                              'round_n': 1,
                              'strategyM': round1Succeed['strategyM'],
                              'strategyF': round1Succeed['strategyF']})

#################################
# %% 问题2.2
# 构建函数


def goLove(dataM, dataF, n):

    dataM['choiceM'] = np.random.choice(dataF.index, len(dataM))
    dataF['choiceF'] = np.random.choice(dataM.index, len(dataF))

    round_match = pd.merge(dataM, dataF, left_on='choiceM', right_index=True).reset_index()

    round_match['score_dis'] = np.abs(round_match['score0'] - round_match['score1'])  # 计算综合评分差值
    round_match['cha_dis'] = np.abs(round_match['character0'] - round_match['character1'])  # 求出内涵得分差值
    round_match['for_dis'] = np.abs(round_match['fortune0'] - round_match['fortune1'])  # 求出财富得分差值
    round_match['app_dis'] = np.abs(round_match['appearances0'] - round_match['appearances1'])  # 求出外貌得分差值

    # 策略0: 一见钟情,男女两者互相喜欢
    round_s0 = round_match[round_match['MId'] == round_match['choiceF']]
    round_s0 = pd.DataFrame({'m': round_s0['MId'],
                             'f': round_s0['choiceM'],
                             'round_n': n,
                             'strategyM': round_s0['strategyM'],
                             'strategyF': round_s0['strategyF'],
                             's0': 1})
    # 因为一见钟情可能是任何形式的择偶,所以先删除
    round_match = round_match.drop(round_s0.index.tolist())

    # 策略1：门当户对，要求双方三项指标加和的总分接近，差值不超过20分；
    round_s1 = round_match[round_match['strategyM'] == 1]  # 筛选男性为策略1的数据
    round_s1['mok'] = 0
    round_s1['fok'] = 0
    # 判断男性的择偶是否符合
    round_s1['mok'][round_s1['score_dis'] <= 20] = 1

    round_sc = pd.DataFrame(columns=round_s1.columns)
    for i, j in round_s1[round_s1['mok'] == 1].groupby('strategyF'):
        if i == 1:
            j['fok'] = 1
            round_sc = pd.concat([round_sc, j])
        elif i == 2:
            j['fok'][j['fortune1'] - j['fortune0'] >= 10] = 1
            round_sc = pd.concat([round_sc, j])
        elif i == 3:
            j['fok'][(j['cha_dis'] < 10) &  # 内涵得分差在10分以内
                     (j['for_dis'] < 5) &  # 财富得分差在5分以内
                     (j['app_dis'] < 5)] = 1  # 外貌得分差在5分以内
            round_sc = pd.concat([round_sc, j])
    round_sc['OK'] = round_sc['mok'] + round_sc['fok']
    round_s1 = round_sc[round_sc['OK'] == 2]

    # 策略2：男才女貌，男性要求女性的外貌分比自己高出至少10分
    round_s2 = round_match[round_match['strategyM'] == 2]
    round_s2['mok'] = 0
    round_s2['fok'] = 0
    # 判断男性的择偶是否符合
    round_s2['mok'][(round_s2['appearances0'] - round_s2['appearances1']) >= 10] = 1  # 男性要求:女性颜值比男性高出至少10分

    round_sc = pd.DataFrame(columns=round_s1.columns)
    for i, j in round_s2[round_s2['mok'] == 1].groupby('strategyF'):
        if i == 1:
            j['fok'][j['score_dis'] <= 20] = 1  # 女性要求:门当户对，要求双方三项指标加和的总分接近，差值不超过20分
            round_sc = pd.concat([round_sc, j])
        elif i == 2:
            j['fok'][j['fortune1'] - j['fortune0'] >= 10] = 1  # 女性要求:男性财富比女性高出至少10分
            round_sc = pd.concat([round_sc, j])
        elif i == 3:
            j['fok'][(j['cha_dis'] < 10) &  # 内涵得分差在10分以内
                     (j['for_dis'] < 5) &  # 财富得分差在5分以内
                     (j['app_dis'] < 5)] = 1  # 外貌得分差在5分以内
            round_sc = pd.concat([round_sc, j])
    round_sc['OK'] = round_sc['mok'] + round_sc['fok']
    round_s2 = round_sc[round_sc['OK'] == 2]

    # 策略3：志趣相投、适度引领，要求对方的内涵得分在比自己低10分~高10分的区间内，且外貌和财富两项与自己的得分差值都在5分以内
    round_s3 = round_match[round_match['strategyM'] == 3]
    round_s3['mok'] = 0
    round_s3['fok'] = 0
    # 判断男性的择偶是否符合
    round_s3['mok'][(round_s3['cha_dis'] < 10) &  # 男性要求:内涵得分差在10分以内
                    (round_s3['for_dis'] < 5) &  # 男性要求:财富得分差在5分以内
                    (round_s3['app_dis'] < 5)] = 1  # 男性要求:女性颜值比男性高出至少10分

    round_sc = pd.DataFrame(columns=round_s1.columns)
    for i, j in round_s3[round_s3['mok'] == 1].groupby('strategyF'):
        if i == 1:
            j['fok'][j['score_dis'] <= 20] = 1  # 女性要求:门当户对，要求双方三项指标加和的总分接近，差值不超过20分
            round_sc = pd.concat([round_sc, j])
        elif i == 2:
            j['fok'][j['fortune1'] - j['fortune0'] >= 10] = 1  # 女性要求:男性财富比女性高出至少10分
            round_sc = pd.concat([round_sc, j])
        elif i == 3:
            j['fok'] = 1  # 女性要求:与男性要求相同
            round_sc = pd.concat([round_sc, j])
    round_sc['OK'] = round_sc['mok'] + round_sc['fok']
    round_s3 = round_sc[round_sc['OK'] == 2]

    # 对配对成功的进行合并,筛选
    roundSucceed = pd.concat([round_s1, round_s2, round_s3])
    roundSucceed = roundSucceed.sort_values(by='score1', ascending=False)  # 如果2男的同时符合1女的要求,选分数最高的
    roundSucceed = roundSucceed.drop_duplicates(subset=['choiceM'], keep='first')

    roundSucceed = pd.DataFrame({'m': roundSucceed['MId'],
                                 'f': roundSucceed['choiceM'],
                                 'round_n': n,
                                 'strategyM': roundSucceed['strategyM'],
                                 'strategyF': roundSucceed['strategyF'],
                                 's0': 0})
    i = len(roundSucceed)
    lov = len(round_s0)
    roundSucceed = pd.concat([roundSucceed, round_s0])
    roundSucceed = roundSucceed.drop_duplicates(subset=['f'], keep='last')

    return i, lov, roundSucceed


print('函数导入完成')

# %% 问题2.2 创建数据
dataM = pd.DataFrame({'fortune1': np.random.exponential(scale=15, size=10000) + 45,
                      'character1': np.random.normal(loc=60, scale=15, size=10000),
                      'appearances1': np.random.normal(loc=60, scale=15, size=10000)},
                     index=['m%i' % i for i in range(1, 10001)])
dataM['score1'] = (dataM['fortune1'] + dataM['character1'] + dataM['appearances1'])
dataM.index.name = 'MId'

dataF = pd.DataFrame({'fortune0': np.random.exponential(scale=15, size=10000) + 45,
                      'character0': np.random.normal(loc=60, scale=15, size=10000),
                      'appearances0': np.random.normal(loc=60, scale=15, size=10000)},
                     index=['f%i' % i for i in range(1, 10001)])
dataF['score0'] = (dataF['fortune0'] + dataF['character0'] + dataF['appearances0'])
dataF.index.name = 'FId'

dataM['strategyM'] = np.random.choice([1, 2, 3], 10000)
dataF['strategyF'] = np.random.choice([1, 2, 3], 10000)

# %% 问题2.2 开始循环
matchSuccess = pd.DataFrame(columns=['m', 'f', 'round_n', 'strategyM', 'strategyF', 's0'])
test_m1 = dataM.copy()
test_f1 = dataF.copy()
# 复制数据

m = 0
n = 1
q = 0
# 设定实验次数变量
starttime = time.time()

while m < 2:  # 出现连续2次没人配对成功的情况下终止循环

    i, l, success_roundn = goLove(test_m1, test_f1, n)
    matchSuccess = pd.concat([matchSuccess, success_roundn])
    test_m1 = test_m1.drop(success_roundn['m'].tolist())
    test_f1 = test_f1.drop(success_roundn['f'].tolist())
    print('成功进行第%i轮实验，本轮实验成功匹配%i对，总共成功匹配%i对，还剩下%i位男性和%i位女性,一见钟情%i对'
          % (n, len(success_roundn), len(matchSuccess), len(test_m1), len(test_f1), l))
    n = n + 1
    q = q + l

    if i == 0:
        m = m + 1
    else:
        m = 0

endtime = time.time()
# 记录结束时间

print('------------')
print('本次实验总共进行了%i轮，配对成功%i对\n------------' % (n, len(matchSuccess)))
print('实验总共耗时%.2f秒' % (endtime - starttime))
print('一见钟情总对数为', q)

del n, m, i, l, q, starttime, endtime, success_roundn
# %%
# 通过数据分析，回答几个问题：
#   ** 百分之多少的样本数据成功匹配到了对象？
#   ** 采取不同择偶策略的匹配成功率分别是多少？
#   ** 采取不同择偶策略的男性各项平均分是多少？

# ① 百分之多少的样本数据成功匹配到了对象？
print('%.2f%%的样本数据成功匹配到了对象\n---------' % (len(matchSuccess) / 10000 * 100))

# ② 采取不同择偶策略的匹配成功率分别是多少？
print('择偶策略1的匹配成功率为%.2f%%'
      % (len(matchSuccess[matchSuccess['strategyM'] == 1]) / len(dataM[dataM['strategyM'] == 1]) * 100))
print('择偶策略2的匹配成功率为%.2f%%'
      % (len(matchSuccess[matchSuccess['strategyM'] == 2]) / len(dataM[dataM['strategyM'] == 2]) * 100))
print('择偶策略3的匹配成功率为%.2f%%'
      % (len(matchSuccess[matchSuccess['strategyM'] == 3]) / len(dataM[dataM['strategyM'] == 3]) * 100))

print('\n---------')

# ③ 采取不同择偶策略的男性各项平均分是多少？
match_m1 = pd.merge(matchSuccess, dataM, left_on='m', right_index=True)
result_df = pd.DataFrame(
    [{
        '财富均值': match_m1[match_m1['strategyM_x'] == 1]['fortune1'].mean(),
        '内涵均值': match_m1[match_m1['strategyM_x'] == 1]['character1'].mean(),
        '外貌均值': match_m1[match_m1['strategyM_x'] == 1]['appearances1'].mean()
    }, {
        '财富均值': match_m1[match_m1['strategyM_x'] == 2]['fortune1'].mean(),
        '内涵均值': match_m1[match_m1['strategyM_x'] == 2]['character1'].mean(),
        '外貌均值': match_m1[match_m1['strategyM_x'] == 2]['appearances1'].mean()
    }, {
        '财富均值': match_m1[match_m1['strategyM_x'] == 3]['fortune1'].mean(),
        '内涵均值': match_m1[match_m1['strategyM_x'] == 3]['character1'].mean(),
        '外貌均值': match_m1[match_m1['strategyM_x'] == 3]['appearances1'].mean()
    }],
    index=['择偶策略1', '择偶策略2', '择偶策略3'])
# 构建数据dataframe

print('择偶策略1的男性 → 财富均值为%.2f，内涵均值为%.2f，外貌均值为%.2f'
      % (result_df.loc['择偶策略1']['财富均值'], result_df.loc['择偶策略1']['内涵均值'], result_df.loc['择偶策略1']['外貌均值']))
print('择偶策略2的男性 → 财富均值为%.2f，内涵均值为%.2f，外貌均值为%.2f'
      % (result_df.loc['择偶策略2']['财富均值'], result_df.loc['择偶策略2']['内涵均值'], result_df.loc['择偶策略2']['外貌均值']))
print('择偶策略3的男性 → 财富均值为%.2f，内涵均值为%.2f，外貌均值为%.2f'
      % (result_df.loc['择偶策略3']['财富均值'], result_df.loc['择偶策略3']['内涵均值'], result_df.loc['择偶策略3']['外貌均值']))
# %%
figQ1 = plt.figure(figsize=(10, 6))
plt.subplots_adjust(hspace=0.3)

ax1 = figQ1.add_subplot(1, 3, 1)
match_m1[['fortune1', 'strategyM_x']].boxplot(by='strategyM_x', ax=ax1, sym='_')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.ylim(0, 150)

ax2 = figQ1.add_subplot(1, 3, 2)
match_m1[['appearances1', 'strategyM_x']].boxplot(by='strategyM_x', ax=ax2, sym='_')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.ylim(0, 150)

ax3 = figQ1.add_subplot(1, 3, 3)
match_m1[['character1', 'strategyM_x']].boxplot(by='strategyM_x', ax=ax3, sym='_')
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.ylim(0, 150)
# 绘制箱型图
# %%
del result_df, match_m1, test_f1, test_m1
dataMQ2 = dataM.copy()
dataFQ2 = dataF.copy()
#################################
# %% 问题3、以100男+100女的样本数据，绘制匹配折线图
'''
3、以99男+99女的样本数据，绘制匹配折线图
要求：
① 生成样本数据，模拟匹配实验
② 生成绘制数据表格
③ bokhe制图
   ** 这里设置图例，并且可交互（消隐模式）
提示：
① bokeh制图时，y轴为男性，x轴为女性
② 绘制数据表格中，需要把男女性的数字编号提取出来，这样图表横纵轴好识别
③ bokhe绘制折线图示意：p.line([0,女性数字编号，女性数字编号],[男性数字编号，男性数字编号，0])

'''
# %%生成样本数据，模拟匹配实验

dataM = pd.DataFrame({'fortune1': np.random.exponential(scale=15, size=100) + 45,
                      'character1': np.random.normal(loc=60, scale=15, size=100),
                      'appearances1': np.random.normal(loc=60, scale=15, size=100)},
                     index=['m%i' % i for i in range(1, 101)])
dataM['score1'] = (dataM['fortune1'] + dataM['character1'] + dataM['appearances1'])
dataM.index.name = 'MId'

dataF = pd.DataFrame({'fortune0': np.random.exponential(scale=15, size=100) + 45,
                      'character0': np.random.normal(loc=60, scale=15, size=100),
                      'appearances0': np.random.normal(loc=60, scale=15, size=100)},
                     index=['f%i' % i for i in range(1, 101)])
dataF['score0'] = (dataF['fortune0'] + dataF['character0'] + dataF['appearances0'])
dataF.index.name = 'FId'

dataM['strategyM'] = np.random.choice([1, 2, 3], 100)
dataF['strategyF'] = np.random.choice([1, 2, 3], 100)

# %%

# 设置好样本数据

dataQ3M = dataM.copy()
dataQ3F = dataF.copy()

matchSuccessQ3 = pd.DataFrame(columns=['m', 'f', 'round_n', 'strategyM', 'strategyF', 's0'])
# 复制数据

m = 0
n = 1
q = 0
# 设定实验次数变量
starttime = time.time()

while m < 2:  # 出现连续2次没人配对成功的情况下终止循环

    i, l, success_roundn = goLove(dataQ3M, dataQ3F, n)
    matchSuccessQ3 = pd.concat([matchSuccessQ3, success_roundn])
    dataQ3M = dataQ3M.drop(success_roundn['m'].tolist())
    dataQ3F = dataQ3F.drop(success_roundn['f'].tolist())
    print('成功进行第%i轮实验，本轮实验成功匹配%i对，总共成功匹配%i对，还剩下%i位男性和%i位女性,一见钟情%i对'
          % (n, len(success_roundn), len(matchSuccessQ3), len(dataQ3M), len(dataQ3F), l))
    n = n + 1
    q = q + l

    if i == 0:
        m = m + 1
    else:
        m = 0

endtime = time.time()
# 记录结束时间

print('------------')
print('本次实验总共进行了%i轮，配对成功%i对\n------------' % (n, len(matchSuccessQ3)))
print('实验总共耗时%.2f秒' % (endtime - starttime))
print('一见钟情总对数为', q)

del n, m, i, l, q, starttime, endtime, dataQ3M, dataQ3F, success_roundn

# %%

picDataQ3 = matchSuccessQ3.copy()
# 生成坐标
picDataQ3['x'] = picDataQ3['m'].str[1:]
picDataQ3['y'] = picDataQ3['f'].str[1:]
# 生成颜色
color = [
    '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d',
    '#a50f15', '#67000d', '#67000d', '#67000d', '#67000d',
    '#67000d', '#67000d', '#67000d', '#67000d', '#67000d',
    '#67000d', '#67000d', '#67000d', '#67000d', '#67000d',
    '#67000d', '#67000d', '#67000d', '#67000d', '#67000d',
    '#67000d', '#67000d', '#67000d', '#67000d', '#67000d',
    '#67000d', '#67000d', '#67000d', '#67000d', '#67000d',
    '#67000d', '#67000d', '#67000d', '#67000d', '#67000d'
]

picDataQ3['color'] = 'blue'
for rn in picDataQ3['round_n'].value_counts().index:
    picDataQ3['color'][picDataQ3['round_n'] == rn] = color[rn - 1]
del rn
picDataQ3['color2'] = 'blue'
picDataQ3['color2'][picDataQ3['s0'] == 1] = 'red'

picDataQ3['leg'] = '非一见钟情'
picDataQ3['leg'][picDataQ3['s0'] == 1] = '一见钟情'

picDataQ3 = picDataQ3.reset_index()
del picDataQ3['index'], color
print('ok')
# %% 绘图
output_file("PJ14Q3_2.html")

p = figure(plot_width=500, plot_height=500, title="配对实验过程模拟示意", tools='reset,wheel_zoom,pan')
# 构建绘图空间

for datai in picDataQ3.index:
    x = picDataQ3.iloc[datai]['x']
    y = picDataQ3.iloc[datai]['y']
    c = picDataQ3.iloc[datai]['color']
    c2 = picDataQ3.iloc[datai]['color2']
    leg = picDataQ3.iloc[datai]['leg']
    # print(x, y)
    p.circle([x, 0, x], [0, y, y], size=3, color=c2, legend=leg)
    p.line([x, x, 0], [0, y, y],
           line_width=1, line_alpha=0.8, line_color=c, legend=leg)

p.ygrid.grid_line_dash = [6, 4]
p.xgrid.grid_line_dash = [6, 4]
p.legend.location = "top_right"
p.legend.click_policy = "hide"

show(p)

print('ok')
# %%
del c, c2, datai, leg, picDataQ3, x, y
##########################################
# %%问题4
'''
4、生成“不同类型男女配对成功率”矩阵图
要求：
① 以之前1万男+1万女实验的结果为数据
② 按照财富值、内涵值、外貌值分别给三个区间，以区间来评判“男女类型”
   ** 高分（70-100分），中分（50-70分），低分（0-50分）
   ** 按照此类分布，男性女性都可以分为27中类型：财高品高颜高、财高品中颜高、财高品低颜高、... （财→财富，品→内涵，颜→外貌）
③ bokhe制图
   ** 散点图
   ** 27行*27列，散点的颜色深浅代表匹配成功率
提示：
① 注意绘图的数据结构
② 这里散点图通过xy轴定位数据，然后通过设置颜色的透明度来表示匹配成功率
③ alpha字段为每种类型匹配成功率标准化之后的结果，再乘以一个参数
   → data['alpha'] = (data['chance'] - data['chance'].min())/(data['chance'].max() - data['chance'].min())*8
'''

# %%
# 数据清洗

picDataQ4 = matchSuccess[matchSuccess['s0'] == 0]
picDataQ4 = pd.merge(picDataQ4, dataMQ2, left_on='m', right_index=True)
picDataQ4 = pd.merge(picDataQ4, dataFQ2, left_on='f', right_index=True)
# 合并数据，得到成功配对的男女各项分值

picDataQ4 = picDataQ4[['m', 'appearances1', 'character1', 'fortune1', 'f', 'appearances0', 'character0', 'fortune0']]
# 筛选字段
picDataQ4['外貌M'] = pd.cut(picDataQ4['appearances1'], [0, 50, 70, 500], labels=['颜低', '颜中', '颜高'])
picDataQ4['内涵M'] = pd.cut(picDataQ4['character1'], [0, 50, 70, 500], labels=['品低', '品中', '品高'])
picDataQ4['资本M'] = pd.cut(picDataQ4['fortune1'], [0, 50, 70, 500], labels=['财低', '财中', '财高'])

picDataQ4['外貌F'] = pd.cut(picDataQ4['appearances0'], [0, 50, 70, 500], labels=['颜低', '颜中', '颜高'])
picDataQ4['内涵F'] = pd.cut(picDataQ4['character0'], [0, 50, 70, 500], labels=['品低', '品中', '品高'])
picDataQ4['资本F'] = pd.cut(picDataQ4['fortune0'], [0, 50, 70, 500], labels=['财低', '财中', '财高'])


# 指标区间划分

picDataQ4['typeM'] = picDataQ4['外貌M'].astype(np.str) + picDataQ4['内涵M'].astype(np.str) + picDataQ4['资本M'].astype(np.str)
picDataQ4['typeF'] = picDataQ4['外貌F'].astype(np.str) + picDataQ4['内涵F'].astype(np.str) + picDataQ4['资本F'].astype(np.str)

picDataQ4 = picDataQ4[['m', 'f', 'typeM', 'typeF']]
# 筛选字段

print(picDataQ4.head())
# %%
# 匹配成功率计算

success_chance = picDataQ4.groupby(['typeM', 'typeF']).count().reset_index()
success_chance['chance'] = success_chance['m'] / len(picDataQ4)
success_chance['alpha'] = (success_chance['chance'] - success_chance['chance'].min()) / (success_chance['chance'].max() - success_chance['chance'].min()) * 8
# 设置alpha参数
success_chance.head()

# %%
# bokeh绘图
output_file("PJ14Q4_2.html")

mlst = success_chance['typeM'].value_counts().index.tolist()
flst = success_chance['typeF'].value_counts().index.tolist()
source = ColumnDataSource(success_chance)    # 创建数据
hover = HoverTool(tooltips=[("男性类别", "@typeM"),
                            ("女性类别", "@typeF"),
                            ("匹配成功率", "@chance")])  # 设置标签显示内容

p = figure(plot_width=800, plot_height=800, x_range=mlst, y_range=flst,
           title="不同类型男女配对成功率", x_axis_label='男', y_axis_label='女',    # X,Y轴label
           tools=[hover, 'reset,wheel_zoom,pan,lasso_select'])   # 构建绘图空间

p.square_cross(x='typeM', y='typeF', size=18, color='red', alpha='alpha', source=source)
# 绘制点

p.ygrid.grid_line_dash = [6, 4]
p.xgrid.grid_line_dash = [6, 4]
p.xaxis.major_label_orientation = "vertical"
# 设置其他参数

show(p)

# %%
del p
