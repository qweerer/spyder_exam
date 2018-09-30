# -*- coding: utf-8 -*-
# %%
# import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

output_file("PJ11_Q2.html")
sns.set_style("whitegrid", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})
# os.chdir('D:\\user\\Documents\\00code\\2018spyder\\项目11国产烂片深度揭秘')
os.chdir('D:\\code\\2018spyder\\项目11国产烂片深度揭秘')
print('导入模块完成')
# %%
data = pd.read_excel('moviedata.xlsx', sheet_name='movies_drop_duplicates2')
data = data[data['豆瓣评分'] > 0]
# 新版pandas要求使用'sheet_name'如果报错请换为下面的代码
# data = pd.read_excel('moviedata.xlsx', sheetname = 'movies_drop_duplicates2')
data_cols = list(data.columns)
dataq1 = data[data["豆瓣评分"].notnull()]
print(dataq1.head())
# %%
fig1 = plt.figure(figsize=(10, 6))
plt.subplots_adjust(hspace=0.2)

ax1 = fig1.add_subplot(2, 1, 1)
plt.hist(dataq1['豆瓣评分'], bins=50,
         edgecolor='black', facecolor='green', alpha=0.5)
plt.grid(linestyle='--', linewidth=0.5, alpha=0.9)
plt.title('豆瓣评分数据分布_直方图')

ax2 = fig1.add_subplot(2, 1, 2)
boxcolor = dict(boxes='DarkGreen', whiskers='orange',
                medians='blue', caps='gray')
dataq1['豆瓣评分'].plot.box(vert=False, color=boxcolor)
plt.grid(linestyle='--', linewidth=0.5, alpha=0.9)
plt.title('豆瓣评分数据分布_箱形图')
del boxcolor
# %%
dataq1_de = dataq1['豆瓣评分'].describe()
dataq1_xi = list(stats.kstest(dataq1['豆瓣评分'], 'norm', (dataq1_de['mean'], dataq1_de['std'])))
print('豆瓣评分的S值为%f,P值为%f' % (dataq1_xi[0], dataq1_xi[1]))
print('豆瓣评分是否呈正太分布为:', dataq1_xi[1] > 0.05)
dataQ1Lan = dataq1[dataq1['豆瓣评分'] < dataq1_de['25%']]
dataQ1Lan = dataQ1Lan.sort_values('豆瓣评分', ascending=True)
print('烂片TOP20为：', '\n', dataQ1Lan.head(20))
del dataq1_xi, dataq1_de
# %% 问题2
# 求烂片类型数据
dataQ2 = dataQ1Lan[['类型', '制片国家/地区']]

dataQ2TypeLan = pd.DataFrame(dataQ2['类型'].str.replace(' ', ''))
dataQ2TypeLan = dataQ2TypeLan['类型'].str.split('/', expand=True).dropna(axis=0, how='all')

dataQ2TpyeLan2 = pd.DataFrame()
for x in dataQ2TypeLan.columns:
    dataQ2TpyeLan2 = pd.concat([dataQ2TpyeLan2, dataQ2TypeLan[x]])

dataQ2TpyeLan2.columns = ['类别']
dataQ2TpyeLan2['烂片计数'] = 1
dataQ2TpyeLan2 = dataQ2TpyeLan2.groupby(['类别']).count()
del dataQ2TypeLan

# 求所有片类型数据
dataQ2 = data[['类型', '制片国家/地区']]

dataQ2TypeAll = pd.DataFrame(dataQ2['类型'].str.replace(' ', ''))
dataQ2TypeAll = dataQ2TypeAll['类型'].str.split('/', expand=True).dropna(axis=0, how='all')

dataQ2TpyeAll2 = pd.DataFrame()
for x in dataQ2TypeAll.columns:
    dataQ2TpyeAll2 = pd.concat([dataQ2TpyeAll2, dataQ2TypeAll[x]])

dataQ2TpyeAll2.columns = ['类别']
dataQ2TpyeAll2['全部计数'] = 1
dataQ2TpyeAll2 = dataQ2TpyeAll2.groupby(['类别']).count()
del dataQ2TypeAll, x

dataQ2 = pd.merge(dataQ2TpyeLan2, dataQ2TpyeAll2,
                  left_index=True, right_index=True)
dataQ2['烂片比例'] = dataQ2['烂片计数'] / dataQ2['全部计数']
dataQ2 = dataQ2.sort_values('烂片比例', ascending=False)
dataQ2 = dataQ2.reset_index()
dataQ2Tu = dataQ2.head(20)
print('烂片比例TOP20为：', '\n', dataQ2Tu)

del dataQ2TpyeAll2, dataQ2TpyeLan2
# %%
dataQ2Tu = dataQ2.head(20)
dataQ2Tu.columns = ['type', 'typeLanCount', 'typeAllCount', 'typeLanPre']

dataQ2Tu['size'] = dataQ2Tu['typeAllCount']**0.5 * 2.5
namelist = list(dataQ2Tu['type'])
source = ColumnDataSource(dataQ2Tu)

hover = HoverTool(tooltips=[('数据量', '@typeAllCount'),
                            ('烂片量', '@typeLanCount'),
                            ('烂片率', '@typeLanPre')])
q2 = figure(plot_width=1000, plot_height=500, x_range=namelist,
            title='不同类型电影烂片比例',
            tools=[hover, 'reset,wheel_zoom,pan,crosshair,save'])
q2.circle(x='type', y='typeLanPre', size='size', source=source,
          fill_color='red', alpha=0.7,
          line_color='black', line_dash=[4, 2], line_width=2)
q2.ygrid.grid_line_dash = [6, 4]
q2.xgrid.grid_line_dash = [6, 4]

show(q2)

# %%
del dataQ2Tu, namelist
# %% 问题3
# 烂片#中有中国的导入
dataQ3 = dataQ1Lan[['类型', '制片国家/地区']]
dataQ3['A'] = dataQ3['制片国家/地区'].str.contains('中国')
dataQ3['B'] = dataQ3['制片国家/地区'].str.contains('香港')
dataQ3['C'] = dataQ3['制片国家/地区'].str.contains('台湾')
dataQ3['A'] = dataQ3['A'] | dataQ3['B'] | dataQ3['C']
dataQ3 = dataQ3[['类型', '制片国家/地区']][dataQ3['A'] > 0]

# #数据整理
dataQ3CunLan = pd.DataFrame(dataQ3['制片国家/地区'].str.replace(' ', ''))
dataQ3CunLan = dataQ3CunLan['制片国家/地区'].str.split('/', expand=True).dropna(axis=0, how='all')

dataQ3CunLan2 = pd.DataFrame()
for x in dataQ3CunLan.columns:
    dataQ3CunLan2 = pd.concat([dataQ3CunLan2, dataQ3CunLan[x]])

# #筛选出烂片中合拍的数据
dataQ3CunLan3 = dataQ3CunLan2.reset_index()
dataQ3CunLan3.columns = ['id', '国家']
dataQ3CunLan3 = dataQ3CunLan3.groupby('id').count()
dataQ3CunLan3 = dataQ3CunLan3[dataQ3CunLan3['国家'] > 1]
dataQ3CunLan2 = pd.merge(dataQ3CunLan2, dataQ3CunLan3, left_index=True, right_index=True)

# #烂片合拍的国家计数
dataQ3CunLan2.columns = ['国家', '烂片计数']
dataQ3CunLan2 = dataQ3CunLan2.groupby('国家').count()

del dataQ3CunLan, dataQ3CunLan3

# 全部#中有中国的导入
dataQ3 = data[['类型', '制片国家/地区']]
dataQ3['A'] = dataQ3['制片国家/地区'].str.contains('中国')
dataQ3['B'] = dataQ3['制片国家/地区'].str.contains('香港')
dataQ3['C'] = dataQ3['制片国家/地区'].str.contains('台湾')
dataQ3['A'] = dataQ3['A'] | dataQ3['B'] | dataQ3['C']
dataQ3 = dataQ3[['类型', '制片国家/地区']][dataQ3['A'] > 0]

# #数据整理
dataQ3CunAll = pd.DataFrame(dataQ3['制片国家/地区'].str.replace(' ', ''))
dataQ3CunAll = dataQ3CunAll['制片国家/地区'].str.split('/', expand=True).dropna(axis=0, how='all')

dataQ3CunAll2 = pd.DataFrame()
for x in dataQ3CunAll.columns:
    dataQ3CunAll2 = pd.concat([dataQ3CunAll2, dataQ3CunAll[x]])

#  #筛选出所有片中合拍的数据
dataQ3CunAll3 = dataQ3CunAll2.reset_index()
dataQ3CunAll3.columns = ['id', '国家']
dataQ3CunAll3 = dataQ3CunAll3.groupby('id').count()
dataQ3CunAll3 = dataQ3CunAll3[dataQ3CunAll3['国家'] > 1]
dataQ3CunAll2 = pd.merge(dataQ3CunAll2, dataQ3CunAll3, left_index=True, right_index=True)

# #全部合拍的国家计数
dataQ3CunAll2.columns = ['国家', '全部计数']
dataQ3CunAll2 = dataQ3CunAll2.groupby('国家').count()
dataQ3CunAll2 = dataQ3CunAll2[dataQ3CunAll2['全部计数'] > 2]

del dataQ3CunAll, x, dataQ3CunAll3

dataQ3 = pd.merge(dataQ3CunLan2, dataQ3CunAll2,
                  left_index=True, right_index=True, how='right')
dataQ3 = dataQ3.fillna(0)
dataQ3 = dataQ3.drop(['中国大陆', '香港', '台湾', '中国']).reset_index()
dataQ3['烂片比例'] = dataQ3['烂片计数'] / dataQ3['全部计数']
dataQ3 = dataQ3.sort_values('烂片比例', ascending=False)


print('合作电影烂片比例TOP：', dataQ3)
del dataQ3CunAll2, dataQ3CunLan2
# %%问题4
dataQ4 = dataQ1Lan[['主演', '豆瓣评分']]

# data为烂片的原始数据
def dataP11One (data,col):
    data = pd.DataFrame(data[col].str.replace(' ', ''))
    data = data[col].str.split('/', expand=True).dropna(axis=0, how='all')
    
    dataLan = pd.DataFrame()
    for x in data.columns:
        dataLan = pd.concat([dataLan, data[x]])
    
    data = dataLan.reset_index()
    data.columns = ['id', col]
    data = data.groupby('id').count()
    dataLan = pd.merge(dataLan, data, left_index=True, right_index=True)
    return dataLan

lllll = dataP11One(data,'主演')
    
    
    
    
# %%    
    
dataQ4ActLan = pd.DataFrame(dataQ4['主演'].str.replace(' ', ''))
dataQ4ActLan = dataQ4ActLan['主演'].str.split('/', expand=True).dropna(axis=0, how='all')

# #数据整理
dataQ4ActLan2 = pd.DataFrame()
for x in dataQ4ActLan.columns:
    dataQ4ActLan2 = pd.concat([dataQ4ActLan2, dataQ4ActLan[x]])

#%%
dataQ4ActLan3 = dataQ4ActLan2.reset_index()
dataQ4ActLan3.columns = ['id', '国家']
dataQ4ActLan3 = dataQ4ActLan3.groupby('id').count()
dataQ4ActLan3 = dataQ4ActLan3[dataQ4ActLan3['国家'] > 1]
dataQ4ActLan2 = pd.merge(dataQ4ActLan2, dataQ4ActLan3, left_index=True, right_index=True)



