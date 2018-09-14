# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})
os.chdir('D:\\code\\2018spyder\\项目12中国城市资本流动问题探索')

print('导入模块成功')
# %%
data = pd.read_excel('data.xlsx',sheet_name='Sheet1')
dataCol = data.columns.tolist()
# %%Q1
dataQ11Sam = data[data['投资方所在城市']==data['融资方所在城市']]
dataQ11Dif = data[data['投资方所在城市']!=data['融资方所在城市']]
dataQ11Sam = dataQ11Sam.groupby(['投资方所在城市','融资方所在城市','年份']).sum().reset_index()
dataQ11Dif = dataQ11Dif.groupby(['投资方所在城市','融资方所在城市','年份']).sum().reset_index()

# %%Q1.1图的数据
dataQ11SamTu = dataQ11Sam[['投资方所在城市','融资方所在城市','投资企业对数']].groupby(['投资方所在城市','融资方所在城市']).sum().sort_values('投资企业对数',ascending=False).head(20)
dataQ11DifTu = dataQ11Dif[['投资方所在城市','融资方所在城市','投资企业对数']].groupby(['投资方所在城市','融资方所在城市']).sum().sort_values('投资企业对数',ascending=False).head(20)
print('投资方，融资方同城TOP20为：\n',dataQ11SamTu)
print('投资方，融资方异城TOP20为：\n',dataQ11DifTu)
# %%Q1.1图
figQ1 = plt.figure(figsize=(20,14))
plt.subplots_adjust(hspace=0.3)

ax1 = figQ1.add_subplot(2,1,1)
dataQ11SamTu.plot(kind = 'bar',ax = ax1,
                  facecolor = 'yellowgreen',alpha=0.8,
                  edgecolor='black',linewidth = 2)

ax2 = figQ1.add_subplot(2,1,2)
dataQ11DifTu.plot(kind = 'bar',ax = ax2,
                  facecolor = 'lightskyblue',alpha=0.8,
                  edgecolor='black',linewidth = 2)