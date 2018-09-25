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
