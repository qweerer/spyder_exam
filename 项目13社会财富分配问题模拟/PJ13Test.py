# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
# 引用自定义函数
import PJ13_function as pjSelf
# os.chdir('D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出')
# os.chdir('.\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出')

print('导入模块完成')
# %%设定初始参数：游戏玩家100人，起始资金100元
person_n = [x for x in range(1, 101)]
fortune = pd.DataFrame([100 for i in range(100)], index=person_n)
fortune.index.name = 'id'

# %%第一轮
fortune[1] = fortune[0] - 1
# 每人拿出一元
gain_r1 = pd.DataFrame({'gain': np.random.choice(person_n, 100)})
gain_r1['+'] = 1
gain_r1 = gain_r1.groupby('gain').count()
# 这一轮中每个人随机指定给“谁”1元钱，并汇总这一轮每个人的盈利情况
fortune = pd.merge(fortune, gain_r1, left_index=True, right_index=True, how='outer')
fortune = fortune.fillna(0)
# 合并数据，得到这一轮每个人“盈”多少钱
fortune[1] = fortune[1] + fortune['+']
del fortune['+'], gain_r1


# %%
del fortune[2]
fortune[1] = pd.DataFrame(pjSelf.processQ1(fortune, 1))
print(fortune[1].sum())

# %% 检验函数代码

ccc = pd.DataFrame({'c': np.random.choice([0, 1], size=100)},
                   index=person_n)
data = fortune.copy()
data[1][ccc['c'] == 0] = 0
print(data[1].sum())
data[2] = pd.DataFrame(pjSelf.processQ1(data, 2))
# %%

datac = pd.DataFrame(data[2][data[2] > 0])
# 财富值大于0的全部减1
datac[3] = datac[2] - 1
# 财富分配，统计
longc = len(datac)
given = pd.DataFrame({'given': np.random.choice(person_n, size=longc)})
given['+'] = 1
given = given.groupby('given').count()

# 财富分配与财富值大于0的合并，
# 采取‘outer’可以使财富值小于0的分配也包含在内，但是需要填充Nan值
datac = pd.merge(datac, given, left_index=True, right_index=True, how='outer')
datac = datac.fillna(0)
datac[3] = datac[3] + datac['+']
data = pd.merge(data, datac[[3, '+']], left_index=True, right_index=True, how='outer')
data = data.fillna(0)
print(data[3].sum())
# %% 检验图片代码


datai = resultQ1.iloc[988]
plt.figure(figsize=(10, 6))
plt.bar(datai.index, datai.values, 
        color='yellowgreen', alpha=0.8, width=0.9,
        edgecolor='black',linewidth=1)
plt.ylim((0, 400))
plt.xlim((-10, 110))
# plt.title('Round %d' % n)
plt.xlabel('PlayerID')
plt.ylabel('Fortune')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
# plt.savefig('graph1_round_%d.png' % n, dpi=200)

# %%
dataf, round_i, person_p4 = fortuneQ4, 239, person_p41

data = pd.DataFrame(dataf[round_i - 1])
data = data.sort_values(by = (round_i - 1))
# 给多少
data['-'] = 1
data['-'][data[round_i - 1] > 230] = np.random.choice([1,2,2,2,2,2,3,3], 
    size = len(data[data[round_i - 1] > 230]))

data['-'][(data[round_i - 1] > 40) & (data[round_i - 1] <= 230)] = np.random.choice([1,1,1,1,2,2,2,3], 
    size = len(data[ (data[round_i - 1] > 40) & (data[round_i - 1] <= 230) ]))

data['-'][data[round_i - 1] <= 40] = np.random.choice([1,1,1,1,1,1,2,2], 
    size = len(data[data[round_i - 1] <= 40]))

# 给谁
given = pd.DataFrame({'given': np.random.choice(person_g, size = 100, p = person_p4)},
                      index=person_n)
given = pd.merge(data, given, left_index=True, right_index=True, how='outer')
given = given[['-','given']].groupby('given').sum()
given.columns = ['+']

# 计算下一回合数
data = data.join(given)
data = data.fillna(0).sort_values(by = 'id')

reQ5sum = sum(data['+'][5:]*0.2)
data['+'][5:] = data['+'][5:]*0.8

# 国家救济与公务员不收税
data['+'][15:20] = 1
data['+'][data[round_i - 1] <= 2] = data['+'][data[round_i - 1] <= 2] + 1
reQ5sum = reQ5sum - len(data['+'][data[round_i - 1] <= 2])

data[round_i] = data[round_i-1] - data['-'] + data['+']
print(data[round_i].sum()+reQ5sum)
# return (data[round_i-1] - data['-'] + data['+']), reQ5sum










