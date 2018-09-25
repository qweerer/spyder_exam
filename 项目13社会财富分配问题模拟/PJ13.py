# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('D:\\code\\2018spyder\\项目13社会财富分配问题模拟\输出')

print('导入模块完成')
# %%设定初始参数：游戏玩家100人，起始资金100元
person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)], index = person_n)
fortune.index.name = 'id'

# %%第一轮
fortune[1] = fortune[0]-1
# 每人拿出一元
gain_r1 = pd.DataFrame({'gain':np.random.choice(person_n,100)})
gain_r1['+'] = 1
gain_r1 = gain_r1.groupby('gain').count()
# 这一轮中每个人随机指定给“谁”1元钱，并汇总这一轮每个人的盈利情况
fortune = pd.merge(fortune,gain_r1,left_index = True,right_index = True,how = 'outer')
fortune = fortune.fillna(0)
# 合并数据，得到这一轮每个人“盈”多少钱
fortune[1] = fortune[1]+fortune['+']
del fortune['+']

# %%
def game1(data, roundi):
    if len(data[data[roundi - 1] ==0]) > 0:   
    # 当数据包含财富值为0的玩家时
        round_i = pd.DataFrame({'pre_round':data[roundi-1],'lost':0})
        con = round_i['pre_round'] > 0
        round_i['lost'][con] = 1               # 设定每轮分配财富之前的情况 → 该轮财富值为0的不需要拿钱给别人
        round_players_i = round_i[con]         # 筛选出参与游戏的玩家：财富值>0
        choice_i = pd.Series(np.random.choice(person_n,len(round_players_i)))
        gain_i = pd.DataFrame({'gain':choice_i.value_counts()})     # 这一轮中每个人随机指定给“谁”1元钱，并汇总这一轮每个人的盈利情况
        round_i = round_i.join(gain_i)
        round_i.fillna(0,inplace = True)
        return round_i['pre_round'] -  round_i['lost'] + round_i['gain']
        # 合并数据，得到这一轮财富分配的结果
    else:
    # 当数据不包含财富值为0的玩家时
        round_i = pd.DataFrame({'pre_round':data[roundi-1],'lost':1}) # 设定每轮分配财富之前的情况
        choice_i = pd.Series(np.random.choice(person_n,100))
        gain_i = pd.DataFrame({'gain':choice_i.value_counts()})       # 这一轮中每个人随机指定给“谁”1元钱，并汇总这一轮每个人的盈利情况
        round_i = round_i.join(gain_i)
        round_i.fillna(0,inplace = True)
        return round_i['pre_round'] -  round_i['lost'] + round_i['gain']
        # 合并数据，得到这一轮财富分配的结果
print('finished!')