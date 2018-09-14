# -*- coding: utf-8 -*-
# %%
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

sns.set_style("whitegrid", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})
os.chdir('D:\\user\\Documents\\00code\\2018spyder\\项目11国产烂片深度揭秘')
# os.chdir('D:\\code\\2018spyder\\项目11国产烂片深度揭秘')
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

# %% 定义一个分类函数


def dataP11One(data, col):
    data = pd.DataFrame(data[col].str.replace(' ', ''))
    data = data[col].str.split('/', expand=True).dropna(axis=0, how='all')

    dataNext = pd.DataFrame()
    for x in data.columns:
        dataNext = pd.concat([dataNext, data[x]])

    data = dataNext.reset_index()
    data.columns = ['id', col]
    data = data.groupby('id').count()
    dataNext = pd.merge(dataNext, data, left_index=True, right_index=True)
    return dataNext


# %% 问题2 数据
# 求烂片类型数据
dataQ2 = dataQ1Lan[['类型', '制片国家/地区']]

dataQ2TypeLan = dataP11One(dataQ2, '类型')
dataQ2TypeLan.columns = ['类型', '烂片计数']
dataQ2TypeLan = dataQ2TypeLan.groupby(['类型']).count()

# 求所有片类型数据
dataQ2TypeAll = dataP11One(dataq1, '类型')
dataQ2TypeAll.columns = ['类型', '全部计数']
dataQ2TypeAll = dataQ2TypeAll.groupby(['类型']).count()

# 最后求出比例
dataQ2 = pd.merge(dataQ2TypeLan, dataQ2TypeAll,
                  left_index=True, right_index=True)
dataQ2['烂片比例'] = dataQ2['烂片计数'] / dataQ2['全部计数']
dataQ2 = dataQ2.sort_values('烂片比例', ascending=False)
dataQ2 = dataQ2.reset_index()
dataQ2Tu = dataQ2.head(20)
print('烂片比例TOP20为：', '\n', dataQ2Tu)

del dataQ2TypeLan, dataQ2TypeAll

# %% 问题2 作图
output_file("PJ11_Q2.html")
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

del dataQ2Tu, namelist

# %% 问题3
# 烂片#中有中国的导入
dataQ3 = dataQ1Lan[['类型', '制片国家/地区']].copy()
dataQ3['A'] = dataQ3['制片国家/地区'].str.contains('中国')
dataQ3['B'] = dataQ3['制片国家/地区'].str.contains('香港')
dataQ3['C'] = dataQ3['制片国家/地区'].str.contains('台湾')
dataQ3['A'] = dataQ3['A'] | dataQ3['B'] | dataQ3['C']
dataQ3 = dataQ3[['类型', '制片国家/地区']][dataQ3['A'] > 0]

# 烂片数据
dataQ3CunLan = dataP11One(dataQ3, '制片国家/地区')
dataQ3CunLan.columns = ['国家/地区', '烂片数量']
dataQ3CunLan = dataQ3CunLan[dataQ3CunLan['烂片数量'] > 1]
dataQ3CunLan = dataQ3CunLan.groupby('国家/地区').count()

# 全部#中有中国的导入
dataQ3 = data[['类型', '制片国家/地区']].copy()
dataQ3['A'] = dataQ3['制片国家/地区'].str.contains('中国')
dataQ3['B'] = dataQ3['制片国家/地区'].str.contains('香港')
dataQ3['C'] = dataQ3['制片国家/地区'].str.contains('台湾')
dataQ3['A'] = dataQ3['A'] | dataQ3['B'] | dataQ3['C']
dataQ3 = dataQ3[['类型', '制片国家/地区']][dataQ3['A'] > 0]

# 烂片数据
dataQ3CunAll = dataP11One(dataQ3, '制片国家/地区')
dataQ3CunAll.columns = ['国家/地区', '全部数量']
dataQ3CunAll = dataQ3CunAll[dataQ3CunAll['全部数量'] > 1]
dataQ3CunAll = dataQ3CunAll.groupby('国家/地区').count()
dataQ3CunAll = dataQ3CunAll[dataQ3CunAll['全部数量'] > 2]

# 求出比例
dataQ3 = pd.merge(dataQ3CunLan, dataQ3CunAll,
                  left_index=True, right_index=True, how='right')
dataQ3 = dataQ3.fillna(0)
dataQ3 = dataQ3.drop(['中国大陆', '香港', '台湾', '中国']).reset_index()
dataQ3['烂片比例'] = dataQ3['烂片数量'] / dataQ3['全部数量']
dataQ3 = dataQ3.sort_values('烂片比例', ascending=False)

del dataQ3CunAll, dataQ3CunLan
print('合作电影烂片比例TOP：', dataQ3)

# %%问题4.1
# 烂片
dataQ4Lan = dataP11One(dataQ1Lan, '主演')
dataQ4Lan = dataQ4Lan.reset_index()
dataQ4Lan.columns = ['id', 'zhu', 'count']
dataQ4Lan2 = dataQ4Lan.drop_duplicates(subset=['id'], keep='first')
dataQ4Lan2['分组'] = pd.cut(dataQ4Lan2['count'], [0, 2, 4, 6, 9, 50], labels=['1-2人', '3-4人', '5-6人', '7-9人', '10人以上'])
dataQ4Lan2 = dataQ4Lan2[['id', '分组']].groupby('分组').count()
dataQ4Lan2.columns = ['烂片数量']

# 全部影片
dataQ4All = dataP11One(dataq1, '主演')
dataQ4All = dataQ4All.reset_index()
dataQ4All.columns = ['id', 'zhu', 'count']
dataQ4All2 = dataQ4All.drop_duplicates(subset=['id'], keep='first')
dataQ4All2['分组'] = pd.cut(dataQ4All2['count'], [0, 2, 4, 6, 9, 100], labels=['1-2人', '3-4人', '5-6人', '7-9人', '10人以上'])

dataQ4All2 = dataQ4All2[['id', '分组']].groupby('分组').count()
dataQ4All2.columns = ['全部数量']

dataQ4 = pd.merge(dataQ4Lan2, dataQ4All2,
                  left_index=True, right_index=True)
dataQ4['烂片率'] = dataQ4['烂片数量'] / dataQ4['全部数量']
print('不同主演数量的烂片率为:', dataQ4)
# %%问题4.2
dataQ4Lan2 = dataQ4Lan.groupby('zhu').count()
del dataQ4Lan2['id']
dataQ4Lan2.columns = ['烂片数量']

dataQ4All2 = dataQ4All.groupby('zhu').count()
del dataQ4All2['id']
dataQ4All2.columns = ['全部数量']

dataQ4 = pd.merge(dataQ4Lan2, dataQ4All2,
                  left_index=True, right_index=True)
dataQ4['烂片率'] = dataQ4['烂片数量'] / dataQ4['全部数量']
dataQ4 = dataQ4.sort_values('烂片率', ascending=False)
print('主演烂片率TOP20为:', dataQ4[dataQ4['烂片数量'] > 2].head(20))

del dataQ4All, dataQ4All2, dataQ4Lan, dataQ4Lan2
# %%问题4.3
print('吴亦凡的烂片率为:', dataQ4[dataQ4.index == '吴亦凡'])
print(dataq1[['电影名称', '主演', '豆瓣评分']][dataq1['主演'].str.contains('吴亦凡').fillna(False)])

# %% 问题5.1
# 问题5初始数据，整理上映时间
dataQ5 = dataq1[['上映日期', '导演', '豆瓣评分']][dataq1['导演'].notnull()]
dataQ5['上映日期'] = dataQ5['上映日期'].str.replace(' ', '')
dataQ5['上映日期'] = dataQ5['上映日期'].str[:4]
dataQ5 = dataQ5[dataQ5['上映日期'].str[0] == '2']
dataQ5['上映日期'] = dataQ5['上映日期'].astype(np.int)

# 对所有影片的导演进行分类，并选出影片数大于等于10的导演
dataQ5All = dataP11One(dataQ5, '导演')
dataQ5All.columns = ['导演', '计数']
dataQ5All1 = dataQ5All.groupby('导演').count()
dataQ5All1 = dataQ5All1.reset_index()
dataQ5All1 = dataQ5All1[dataQ5All1['计数'] > 9]

# 对烂片片的导演进行分类
dataQ5All = dataQ5All.reset_index()
dataQ5All2 = pd.merge(dataQ5All[['导演', 'index']], dataQ5All1, on='导演')
dataQ5Lan2 = pd.merge(dataQ1Lan[['电影名称', '类型']], dataQ5All2, left_index=True, right_on='index')
dataQ5Lan2 = dataQ5Lan2.groupby('导演').count()

# 求处烂片率
dataQ5All1.columns = ['导演', '全部计数']
dataQ5Lan1 = pd.DataFrame(dataQ5Lan2['计数'])
dataQ5Lan1.columns = ['烂片计数']
dataQ51 = pd.merge(dataQ5All1, dataQ5Lan1, left_on='导演', right_index=True, how='left').fillna(0)
dataQ51['烂片比例'] = dataQ51['烂片计数'] / dataQ51['全部计数']
dataQ51 = dataQ51.sort_values('烂片比例', ascending=False)

del dataQ5All1, dataQ5All2, dataQ5Lan1, dataQ5Lan2
# 我的比老师的少一个徐克，因为老师的方法中，在计算徐克的时候，把（小）徐克也算在内了
# %% 问题5.2 创建图表数据

dataQ51 = dataQ51[dataQ51['烂片计数'] > 0]
dataQ5tu = {}
for x in dataQ51['导演']:
    '''dataQ52位为一个导演所拍的所有电影，电影ID在index列'''
    dataQ52 = dataQ5All[dataQ5All['导演'] == x]
    '''根据ID得到电影的上映日期与豆瓣评分'''
    dataQ52All = pd.merge(dataQ52, dataQ5[['上映日期', '豆瓣评分']], left_on='index', right_index=True, how='left')
    dataQ521 = dataQ52All[['计数', '上映日期']].groupby('上映日期').count()
    dataQ522 = dataQ52All[['豆瓣评分', '上映日期']].groupby('上映日期').mean()
    dataQ52 = pd.merge(dataQ521, dataQ522, left_index=True, right_index=True, how='outer')
    dataQ52 = dataQ52[dataQ52.index > 2007]
    dataQ52 = dataQ52.reset_index()
    dataQ52.columns = ['years', 'num', 'score']
    dataQ52['num'] = dataQ52['num']**0.5 * 13
    dataQ5tu.update({x: dataQ52})

del dataQ52All, dataQ52, dataQ521, dataQ522, x
# %% 问题5
output_file("PJ11_Q5.html")

color = ['green', 'blue', 'red']
hover = HoverTool(tooltips=[('电影均分', '@score'),
                            ('这一年电影产量', '@num')])
q5 = figure(plot_width=1500, plot_height=400,
            title='不同导演每年的电影产量及电影均分',
            tools=[hover, 'reset,wheel_zoom,pan,crosshair,box_select,save'])
i = 0
for x in dataQ5tu:
    source = ColumnDataSource(dataQ5tu[x])
    q5.circle(x='years', y='score', size='num', source=source,
              fill_color=color[i], fill_alpha=0.6,
              line_color='black', line_alpha=0.8, line_width=0.5, line_dash=[4, 2])
    i = i + 1


show(q5)
