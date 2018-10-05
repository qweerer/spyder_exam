import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print('导入模块完成,PJ13函数')

person_n = [x for x in range(1, 101)]
# 第三问需要的常数
person_p = [0.899 / 90 for i in range(100)]
for i in [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]:
    person_p[i - 1] = 0.0101
# 第四问需要的常数
person_g = person_n.copy()
del person_g[15:20]

# %% 设置过程函数（当资金为0时不支出）


def processQ1(dataf, round_i):
    data = dataf.copy()
    if len(data[data[round_i - 1] == 0] > 0):
        datac = pd.DataFrame(data[round_i - 1][data[round_i - 1] > 0])
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
        data = pd.merge(data, datac[[round_i, '+']], left_index=True, right_index=True, how='outer')
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

# %% 设置过程函数（当资金为0时可以借贷）


def processQ2(dataf, round_i):
    data = dataf.copy()
    data[round_i] = data[round_i - 1] - 1

    given = pd.DataFrame({'given': np.random.choice(person_n, 100)})
    given['+'] = 1
    given = given.groupby('given').count()

    data = pd.merge(data, given, left_index=True, right_index=True, how='outer')
    data = data.fillna(0)
    data[round_i] = data[round_i] + data['+']

    return data[round_i]

# %% 设置过程函数 可以借贷 有给钱倾向


def processQ3(dataf, round_i):
    data = dataf.copy()
    data[round_i] = data[round_i - 1] - 1

    given = pd.DataFrame({'given': np.random.choice(person_n, size=100, p=person_p)})
    given['+'] = 1
    given = given.groupby('given').count()

    data = pd.merge(data, given, left_index=True, right_index=True, how='outer')
    data = data.fillna(0)
    data[round_i] = data[round_i] + data['+']

    return data[round_i]

# %% 设置过程函数 可以借贷 有给钱倾向 根据答案代码进行优化 但并没有太多运行效率提升


def processQ4(dataf, round_i):
    data = dataf.copy()
    data[round_i] = data[round_i - 1] - 1

    given = pd.Series(np.random.choice(person_n, size=100, p=person_p))
    given = pd.DataFrame({'+': given.value_counts()})

    data = data.join(given)
    data = data.fillna(0)

    return data[round_i] + data['+']

# %% 设置过程函数 自建模型


def processQ5(dataf, round_i, person_p4):
    data = pd.DataFrame(dataf[round_i - 1])
    data = data.sort_values(by=(round_i - 1))
    # 给多少
    data['-'] = 1
    data['-'][data[round_i - 1] > 230] = np.random.choice([1, 2, 2, 2, 2, 3, 3, 3],
                                                          size=len(data[data[round_i - 1] > 230]))

    data['-'][(data[round_i - 1] > 40) & (data[round_i - 1] <= 230)] = np.random.choice([1, 1, 1, 2, 2, 2, 2, 3],
                                                                                        size=len(data[(data[round_i - 1] > 40) & (data[round_i - 1] <= 230)]))

    data['-'][data[round_i - 1] <= 40] = np.random.choice([1, 1, 1, 1, 1, 1, 2, 2],
                                                          size=len(data[data[round_i - 1] <= 40]))

    # 给谁
    given = pd.DataFrame({'given': np.random.choice(person_g, size=100, p=person_p4)},
                         index=person_n)
    given = pd.merge(data, given, left_index=True, right_index=True, how='outer')
    given = given[['-', 'given']].groupby('given').sum()
    given.columns = ['+']

    # 计算下一回合数
    data = data.join(given)
    data = data.fillna(0).sort_values(by='id')

    # 收税
    reQ5sum = sum(data['+'][5:] * 0.051)
    data['+'][5:] = data['+'][5:] * 0.949000000000001

    # 国家救济与公务员不收税
    data['+'][15:20] = 1.63
    data['+'][data[round_i - 1] <= 2] = data['+'][data[round_i - 1] <= 2] + 1
    reQ5sum = reQ5sum - len(data['+'][data[round_i - 1] <= 2])

    return (data[round_i - 1] - data['-'] + data['+']), reQ5sum
# %% 设置输出函数-没有按财富值排序


def Pic1(data, start, end, length, theMax):
    for n in list(range(start, end, length)):
        datai = data.iloc[n]
        plt.figure(figsize=(10, 6))
        plt.bar(datai.index, datai.values,
                color='yellowgreen', alpha=0.8, width=0.9,
                edgecolor='black', linewidth=1)
        plt.ylim((0, theMax))
        plt.xlim((-5, 105))
        plt.title('Round %d' % n)
        plt.xlabel('PlayerID')
        plt.ylabel('Fortune')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.savefig('graph1_round_%d.png' % n, dpi=200)
# 创建绘图函数1
# %% 设置输出函数-按财富值排序


def Pic2(data, start, end, length, theMax, theMin):
    for n in list(range(start, end, length)):
        datai = data.iloc[n].sort_values().reset_index()[n]
        plt.figure(figsize=(10, 6))
        plt.bar(datai.index, datai.values,
                color='yellowgreen', alpha=0.8, width=0.9,
                edgecolor='black', linewidth=1)
        plt.ylim((theMin, theMax))
        plt.xlim((-5, 105))
        plt.title('Round %d' % n)
        plt.xlabel('PlayerID')
        plt.ylabel('Fortune')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.savefig('graph2_round_%d.png' % n, dpi=200)
# 创建绘图函数2

# %% 设置输出函数-按财富值排序,有颜色判断,数据不能转置


def Pic3(data, start, end, length, theMax, theMin):
    for n in list(range(start, end, length)):
        datai = data[[n, 'color']].sort_values(by=(n)).reset_index()[[n, 'color']]
        plt.figure(figsize=(10, 6))
        plt.bar(datai.index, datai[n],
                color=datai['color'], alpha=0.8, width=0.9,
                edgecolor='black', linewidth=1)
        plt.ylim((theMin, theMax))
        plt.xlim((-5, 105))
        plt.title('Round %d' % n)
        plt.xlabel('PlayerID')
        plt.ylabel('Fortune')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.savefig('graph2_round_%d.png' % n, dpi=200)
# 创建绘图函数3
