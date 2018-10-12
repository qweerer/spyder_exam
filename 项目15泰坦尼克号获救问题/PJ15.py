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

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
sns.set_style("white", {"font.sans-serif": ['simhei', 'Arial']})
# sns.set_context("talk")
plt.rcParams['axes.unicode_minus'] = False

# os.chdir('D:/user/Documents/00code/spyder_exam/项目15泰坦尼克号获救问题')
os.chdir('/home/qweerer/0code/spyder_exam/项目15泰坦尼克号获救问题')

pathPj15 = os.path.abspath('.')
print('导入模块完成')

#################################
# %%导入
testData = pd.read_csv('test.csv', engine='python')
trainData = pd.read_csv('train.csv', engine='python')
os.chdir('%s/输出' % pathPj15)

# %%问题1
picDataQ1 = trainData['Survived'].value_counts()
picDataQ1.index = ['未能获救', '获救']

plt.title('泰坦尼克号存活比例')

plt.axis('equal')
plt.pie(picDataQ1,
        labels=picDataQ1.index,
        colors=['#FFCCCC', '#0099CC'],
        autopct='%.2f%%',
        shadow=True,
        startangle=90,
        explode=[0.1, 0])

print('存活比例为%.2f%%' % ((picDataQ1['获救'] * 100) / (picDataQ1['未能获救'] + picDataQ1['获救'])))

plt.savefig('PJ15Q1.png', dpi=200)

del picDataQ1
# %% 问题2
'''
2、结合性别和年龄数据，分析幸存下来的人是哪些人？
要求：
① 年龄数据的分布情况
② 男性和女性存活情况
③ 老人和小孩存活情况
'''
# %% 2.1 年龄
picDataQ2 = trainData[['Age', 'Sex', 'Survived', 'Pclass']]

picDataQ21 = picDataQ2[['Age', 'Survived']].dropna(axis=0, how='any')

picDataQ21Des = picDataQ21['Age'].describe()
print('关于年龄的分布数据为:')
print(picDataQ21Des)

picDataQ21['Survived'][picDataQ21['Survived'] == 1] = '幸存'
picDataQ21['Survived'][picDataQ21['Survived'] == 0] = '死亡'
# picDataQ21['Age'] = picDataQ21['Age'].astype('float')

del picDataQ21Des
# %%
figQ21 = plt.figure(figsize=(12, 5))
plt.subplots_adjust(wspace=0.2)

ax1 = figQ21.add_subplot(1, 2, 1)
plt.hist(picDataQ21['Age'], bins=50, histtype='bar',
         edgecolor='black', alpha=0.7)
plt.grid(color='grey', linestyle=':', linewidth=1, axis='both')

ax2 = figQ21.add_subplot(1, 2, 2)
sns.boxplot(x='Survived', y='Age', data=picDataQ21,
            width=0.3, fliersize=1, palette=['#FFCCCC', '#0099CC'])
sns.swarmplot(x="Survived", y="Age", data=picDataQ21,
              palette=['red', 'blue'], size=3, alpha=0.4)

plt.savefig('PJ15Q2.1.png', dpi=200)

del picDataQ21
# %% 2.2 性别
picDataQ22 = picDataQ2[['Sex', 'Survived']].dropna(axis=0, how='any')

picDataQ22['count'] = 1
picDataQ22 = picDataQ22.groupby(['Sex', 'Survived']).count().reset_index()
print(picDataQ22)

f = picDataQ22['count'][1] / (picDataQ22['count'][0] + picDataQ22['count'][1])
m = picDataQ22['count'][3] / (picDataQ22['count'][2] + picDataQ22['count'][3])

picDataQ22 = pd.Series({'女性存活率': f,
                        '男性存活率': m})
figQ22 = plt.figure(figsize=(6, 5))
picDataQ22.plot(kind='bar', color='orange', alpha=0.7,
                edgecolor='black', rot=0)
plt.grid(color='grey', linestyle=':', linewidth=1, axis='both')
plt.title('男女的存活比例')

print('女性存活率为%.2f' % f)
print('男性存活率为%.2f' % m)

del f, m, picDataQ22
# %% 2.3 船舱等级
picDataQ23 = picDataQ2.copy()

picDataQ23 = picDataQ23[picDataQ23["Age"].notnull()]

picDataQ23['Survived'][picDataQ23['Survived'] == 1] = '幸存'
picDataQ23['Survived'][picDataQ23['Survived'] == 0] = '死亡'

figQ23 = plt.figure(figsize=(14, 6))
plt.subplots_adjust(wspace=0.1)

ax1 = figQ23.add_subplot(1, 2, 1)
sns.violinplot(x='Pclass', y='Age', hue='Survived', data=picDataQ23,
               split=True, palette=['#FF9273', '#00B454'], scale='count')

ax2 = figQ23.add_subplot(1, 2, 2)
sns.violinplot(x='Sex', y='Age', hue='Survived', data=picDataQ23,
               split=True, palette=['#FF9273', '#00B454'], scale='count')

plt.savefig('PJ15Q2.3.png', dpi=200)
del picDataQ23
# %% 2.4 按年龄分布的幸存率
picDataQ24 = picDataQ2[['Age', 'Survived']]
picDataQ24 = picDataQ24[picDataQ24["Age"].notnull()]
picDataQ24['Age'] = picDataQ24['Age'].astype('int')
picDataQ24 = picDataQ24.groupby('Age').agg(['count', 'sum'])
picDataQ24.columns = ['count', 'sum']
picDataQ24['survived'] = picDataQ24['sum'] / picDataQ24['count']

figQ24 = plt.figure(figsize=(14, 4))
sns.barplot(x=picDataQ24.index, y="survived", data=picDataQ24,
            palette='BuPu', edgecolor='black')
plt.grid(color='grey', linestyle=':', linewidth=1, axis='both')
plt.savefig('PJ15Q2.4.png', dpi=200)
del picDataQ24, picDataQ2
# %% 3
picDataQ3 = trainData[['Survived', 'SibSp', 'Parch']]
