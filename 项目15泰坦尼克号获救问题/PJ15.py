# -*- coding: utf-8 -*-
# %%
import os
import time

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pylab import mpl
import seaborn as sns


# 导入图表绘制、图标展示模块

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
sns.set_style("ticks",{"font.sans-serif":['simhei','Arial']})
sns.set_context("talk")
plt.rcParams['axes.unicode_minus'] = False

# os.chdir('D:/user/Documents/00code/spyder_exam/项目15泰坦尼克号获救问题/输出')
# os.chdir('/home/qweerer/0code/spyder_exam/项目15泰坦尼克号获救问题')

# pathPj15 = os.path.abspath('.')
print('导入模块完成')

#################################
# %%问题1
testData = pd.read_csv('test.csv', engine='python')
trainData = pd.read_csv('train.csv', engine='python')
sns.set()


picDataQ1 = trainData['Survived'].value_counts()
picDataQ1.index = ['未能获救', '获救']

plt.axis('equal')
picDataQ1.plot.pie(autopct='%1.2f%%')
print('存活比例为38.38%')
