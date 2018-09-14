# -*- coding: utf-8 -*-
# %%
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bokeh.plotting import figure,show,output_file
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
# 导入图表绘制、图标展示模块
# output_file → 非notebook中创建绘图空间
sns.set_style("ticks", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False
os.chdir('D:\\user\\Documents\\00Py学习\\spyder\\ch7 pj10')
print('导入模块完成')
# %%
data0 = pd.read_csv('house_rent.csv', engine='python')
data1 = pd.read_csv('house_sell.csv', engine='python')
data0 = data0[data0["lat"].notnull() & data0["lng"].notnull() & data0["price"].notnull() & data0["area"].notnull()]
data1 = data1[data1["lat"].notnull() & data1["lng"].notnull() & data1["average_price"].notnull()]
data0['rent_area'] = data0['price'] / data0['area']
# %%
data01 = data0[['community', 'rent_area', 'lng', 'lat']].groupby('community').mean()
data11 = data1[['property_name', 'average_price']].groupby('property_name').mean()
dataq1 = pd.merge(data01, data11, left_index=True, right_index=True)
del data11, data01
dataq1.reset_index(inplace=True)
# %% 问题2
dataq1['z_s'] = dataq1['rent_area'] / dataq1['average_price']
dataq1 = dataq1[dataq1['z_s'] != np.inf]

# %%
fig = plt.figure(figsize=(20, 8))
plt.subplots_adjust(hspace=0.3)


ax1 = fig.add_subplot(2, 1, 1)
plt.hist(dataq1['z_s'], bins=100, histtype='bar',
         facecolor='green', edgecolor='#7ECEC0', alpha=0.7)
sns.despine()
plt.grid(color='grey', linestyle='--', linewidth=1, axis='y')
plt.title('房屋租售比_直方图')

ax2 = fig.add_subplot(2, 1, 2)
sns.boxplot(x='z_s', data=dataq1, whis=3, color='#25B6D0')
sns.despine()
plt.grid(color='grey', linestyle='--', linewidth=1, axis='y')
plt.title('房屋租售比_箱形图')

# %%
dataq1.to_csv("rent_sell.csv", encoding='utf_8')
# %%
dataq3 = pd.read_csv('PJ10Q3.csv', encoding='utf_8')
dataq3.columns = ['人口密度', '交通', '餐饮', '餐饮人均', '采集房屋数量', '平均租金', '平均房价', '平均租售比', 'lng', 'lat']
del dataq3['餐饮'], dataq3['采集房屋数量']
dataq3['中心点距离'] = ((dataq3['lng'] - 353508.848122)**2 + (dataq3['lat'] - 3456140.926976)**2)**0.5

dataq3 = dataq3.fillna(0)
dataq3 = dataq3[dataq3['平均租售比'] != 0]


def data_norm(df, *cols):
    df_n = df.copy()
    for col in cols:
        ma = df_n[col].max()
        mi = df_n[col].min()
        df_n[col] = (df_n[col] - mi) / (ma - mi)
    return(df_n)


dataq3 = data_norm(dataq3, '人口密度', '交通', '餐饮人均')
# %%

fig = plt.figure(figsize=(10, 12))
plt.subplots_adjust(hspace=0.3)

ax1 = fig.add_subplot(4, 1, 1)
dataq31 = dataq3[dataq3['人口密度'] != 0]
plt.scatter(dataq31['人口密度'], dataq31['平均房价'],
            marker='.', s=5, c='#258EDF', alpha=0.5)
plt.xlabel('人口密度指标')
plt.ylabel('房屋每平米均价')
plt.grid(linestyle='--')


ax2 = fig.add_subplot(4, 1, 2)
dataq31 = dataq3[dataq3['交通'] != 0]
plt.scatter(dataq31['交通'], dataq31['平均房价'],
            marker='.', s=5, c='#9CD864', alpha=0.5)
plt.xlabel('交通指标')
plt.ylabel('房屋每平米均价')
plt.grid(linestyle='--')


ax3 = fig.add_subplot(4, 1, 3)
dataq31 = dataq3[dataq3['餐饮人均'] != 0]
plt.scatter(dataq31['餐饮人均'], dataq31['平均房价'],
            marker='.', s=5, c='#ED703A', alpha=0.5)
plt.xlabel('餐饮人均指标')
plt.ylabel('房屋每平米均价')
plt.grid(linestyle='--')


ax4 = fig.add_subplot(4, 1, 4)
plt.scatter(dataq31['中心点距离'], dataq31['平均房价'],
            marker='.', s=5, c='#B61BA8', alpha=0.5)
plt.xlabel('中心点距离指标')
plt.ylabel('房屋每平米均价')
plt.grid(linestyle='--')

print(dataq3[['人口密度', '交通', '餐饮人均', '中心点距离', '平均房价']].corr().loc['平均房价'])
# %%
# dataq3['距市中心距离'] = pd.cut(dataq3['中心点距离'], [x*10000 for x in range(7)], labels=[x*10000+10000 for x in range(6)])

# %%
dataq4 = dataq3[['人口密度', '交通', '餐饮人均', '中心点距离', '平均房价']]

dataq41 = pd.DataFrame()
y = 0
for x in [1,2,3,4,5,6]:
    y = x*10000
    z = dataq4[dataq4['中心点距离'] < y].corr().rename(columns = {'平均房价':y})[y]
    dataq41 = pd.concat([dataq41,z], axis=1)

dataq41 = dataq41.T
del dataq41['平均房价']
dataq41 = dataq41.reset_index()
dataq41.columns = ['jl','leng','jt','rk','cy']

# %%

output_file("PJ10.html")
source = ColumnDataSource(data = dataq41)
hover = HoverTool(tooltips=[("距离中心点的距离", "@jl"),
                            ("人口密度相关系数", "@rk"),
                            ("距离中心点距离相关系数", "@leng"),
                            ("交通线路相关系数", "@jt"),
                            ("餐饮消费相关系数", "@cy")])
q4 = figure(plot_width=1000, plot_height=400,
            title = '随着逐渐远离市中心,不同指标的相关系变化',
            tools = [hover,'reset,xwheel_zoom,pan,crosshair,box_select,save'])

q4.line(x='jl',y='rk',source = source, legend="人口密度相关系数",
       line_width=1, line_alpha = 0.8, line_color = 'black',line_dash = [10,5])
q4.circle(x='jl',y='rk',source = source, legend="人口密度相关系数",
          size = 10,color = 'black',alpha = 0.8)

q4.line(x='jl',y='leng',source = source, legend="距离中心点距离相关系数",
       line_width=1, line_alpha = 0.8, line_color = 'red',line_dash = [10,5])
q4.circle(x='jl',y='leng',source = source, legend="距离中心点距离相关系数",
          size = 10,color = 'red',alpha = 0.8)

q4.line(x='jl',y='jt',source = source, legend="交通线路相关系数",
       line_width=1, line_alpha = 0.8, line_color = 'green',line_dash = [10,5])
q4.circle(x='jl',y='jt',source = source, legend="交通线路相关系数",
          size = 10,color = 'green',alpha = 0.8)

q4.line(x='jl',y='cy',source = source, legend="餐饮消费相关系数",
       line_width=1, line_alpha = 0.8, line_color = 'blue',line_dash = [10,5])
q4.circle(x='jl',y='cy',source = source, legend="餐饮消费相关系数",
          size = 10,color = 'blue',alpha = 0.8)
q4.legend.location = "center_right"
show(q4)





