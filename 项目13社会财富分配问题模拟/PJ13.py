# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('D:\\code\\2018spyder\\项目13社会财富分配问题模拟\输出')

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


def process(dataf, round_i):
    data = dataf.copy()
    if len(data[data[round_i - 1] == 0] > 0):
        datac = data[round_i - 1][data[round_i - 1] > 0]
        # 财富值大于0的全部减1
        datac[round_i] = datac[round_i - 1] - 1
        # 财富分配，统计
        longc = len(datac)
        given = pd.DataFrame({'given': np.random.choice(person_n, size=longc)})
        given['+'] = 1
        given = given.groupby('given').count()
        # 财富分配与财富值大于0的合并，
        # 采取‘outer’可以使财富值小于0的分配也包含在内，但是需要填充Nan值
        datac = pd.merge(datac, given, left_index=True, right_index=True, how='outer')
        datac = datac.fillna(0)
        datac[round_i] = datac[round_i] + datac['+']
        # datac与data(源数据)合并
        data = pd.merge(data, datac[[3, '+']], left_index=True, right_index=True, how='outer')
        data = data.fillna(0)

    else:
        data[round_i] = data[round_i - 1] - 1

        given = pd.DataFrame({'given': np.random.choice(person_n, 100)})
        given['+'] = 1
        given = given.groupby('given').count()

        data = pd.merge(data, given, left_index=True, right_index=True, how='outer')
        data = data.fillna(0)
        data[round_i] = data[round_i] + data['+']

    return data[round_i]


# %%
del fortune[2]
fortune[2] = pd.DataFrame(process(fortune, 2))
print(fortune[2].sum())

# %% 检验代码

ccc = pd.DataFrame({'c': np.random.choice([0, 1], size=100)},
                   index=person_n)
data = fortune.copy()
data[2][ccc['c'] == 0] = 0
print(data[2].sum())
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
