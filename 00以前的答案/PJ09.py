# %%  导入模块
import os
# import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
print('导入模块成功')
# %% 导入数据
os.chdir('D:\\user\\Documents\\00Py学习\\spyder\\ch7 pj09')
data = pd.read_csv('data01.csv', engine='python', encoding='UTF-8')
data02 = pd.read_csv('data01.csv', engine='python', encoding='UTF-8')
data02 = pd.concat([data, data02])
data02['工作地'] = data02['工作地'].str[:20]
data = pd.read_excel('中国行政代码对照表.xlsx', Sheels=0)

data['行政编码'] = data['行政编码'].astype(str)
data02['户籍地城市编号'] = data02['户籍地城市编号'].astype(str)
data02 = pd.merge(data02, data, left_on='户籍地城市编号', right_on='行政编码')
print(data02.head(), '\n', len(data02))
print('导入数据完毕')
del data02['户籍地城市编号'], data02['行政编码'], data
# del data02
# %%
# data_count = data.groupby('姓').count()
# print('所有的姓氏总数为%i' % len(data_count), '个')
# data02 = data021.head(400000)
data02['省2'] = data02['工作地'].str.split('省').str[0]
data02['省_自治区'] = data02['工作地'].str.split('自治区').str[0]
data02['省_维吾尔'] = data02['工作地'].str.split('维吾尔族自治区').str[0]
# data02['省'] = 0
data02['工作地_省'] = data02['省2']
data02['工作地_省'][data02['工作地_省'].str.len() > 4] = data02['省_自治区']
data02['工作地_省'][data02['工作地_省'].str.len() > 4] = data02['省_维吾尔']
data02['工作地_省'][data02['工作地_省'].str.len() > 4] = data02['省2']

data02['工作地_市'] = data02['工作地'].str.split('省').str[1].str.split('市').str[0]
data02['工作地_市'][data02['省2'].str.len() > 4] = data02['工作地'].str.split('市').str[0]
data02['工作地_市'][data02['省_自治区'].str.len() < 4] = data02['工作地'].str.split('自治区').str[1].str.split('市').str[0]

data02['工作地_县(区)'] = ''
data02['工作地_县(区)'][(data02['工作地_市'].str.len() < 5) & (data02['工作地'].str.contains('区'))] = data02['工作地'].str.split('市').str[1].str.split('区').str[0]
data02['工作地_县(区)'][(data02['工作地_市'].str.len() > 4) & (data02['工作地'].str.contains('区'))] = data02['工作地'].str.split('区').str[0] + '区'
data02['工作地_县(区)'][(data02['工作地_市'].str.len() < 5) & (data02['工作地'].str.contains('县'))] = data02['工作地'].str.split('市').str[1].str.split('县').str[0]
data02['工作地_县(区)'][(data02['工作地_市'].str.len() > 4) & (data02['工作地'].str.contains('县'))] = data02['工作地'].str.split('县').str[0] + '县'

data02['工作地_省'][data02['工作地_省'].str.len() > 4] = '未识别'
data02['工作地_市'][data02['工作地_市'].str.len() > 5] = '未识别'
data02['工作地_县(区)'][(data02['工作地_县(区)'].str.len() > 5) | (data02['工作地_县(区)'].str.len() < 2)] = '未识别'

del data02['省_维吾尔'], data02['省2'], data02['省_自治区'], data02['工作地']
# data.columns = ['姓','户籍所在地编号','工作地','户籍所在地_省','户籍所在地_市','户籍所在地_区县','户籍所在地_lng','户籍所在地_lat','工作地_省','工作地_市','工作地_区县']
# data02['市'][data02['省_维吾尔'].str.len()<4] = data02['工作地'].str.split('维吾尔族自治区').str[1].str.split('市').str[0]
# data02['区'] =
# data02['省2'] = data02['工作地'].str.split('省').str[0]
# %% 问题2 1.输出EXL
data = data02[data02['姓'] == '王']
data = data.groupby(['姓','lng','lat'])['市'].count()
data = data.reset_index()
writer = pd.ExcelWriter('王姓.xlsx')
data.to_excel(writer, 'shell1')
writer.save()
data = data02[data02['姓'] == '姬']
data = data.groupby(['姓','lng','lat'])['市'].count()
data = data.reset_index()
writer = pd.ExcelWriter('姬姓.xlsx')
data.to_excel(writer, 'shell1')
writer.save()

# %%
print(data02.head())
# %%
data = data02[['姓', '省']].groupby('姓').count().sort_values('省', ascending=False)
data['和'] = data['省'].sum()
data['姓分'] = data['省'] / data['和']
data = data.head(20)
data.index.name = 'index'
del data['和']
print(data)
# %%

output_file("Q2.html")

data.columns = ['num','num_c']

namelst = data.index.tolist()
source = ColumnDataSource(data)

hover = HoverTool(tooltips = [('姓氏数目为','@num')])
q21 = figure(plot_width=800, plot_height=250,x_range = namelst,
             title = '姓氏top20计数',
             tools = [hover,'reset,xwheel_zoom,pan,crosshair,box_select,save'])
q21.vbar(x = 'index', 
         top = 'num', 
         width = 0.8, 
         source = source,
         
         color = 'red',
         alpha = 0.7,
         
         line_width = 1, 
         line_alpha = 0.8, 
         line_color = 'black', 
         line_dash = [5,2])

hover = HoverTool(tooltips = [('姓氏占比为','@num_c')])
q22 = figure(plot_width=800, plot_height=250,x_range=q21.x_range,
             title = '姓氏top20占比',
             tools = [hover,'reset,xwheel_zoom,pan,crosshair,box_select'])
q22.vbar(x = 'index', 
         top = 'num_c', 
         width = 0.8, 
         source = source,
         
         color = 'blue',
         alpha = 0.7,
         
         line_width = 1, 
         line_alpha = 0.8, 
         line_color = 'black', 
         line_dash = [5,2])

q2 = gridplot([[q21],[q22]])
show(q2)
# %%
data = data02[(data02['姓'] == '陶') & (data02['工作地_市'] != '未识别') & (data02['工作地_县(区)'] != '未识别')]
data = data[(data['区/县'] != data['工作地_县(区)']) & (data['lat'] != -1)]

del data['省'],data['市'],data['区/县']
data.columns = ['name','lng','lat','sheng','shi','qu']
writer = pd.ExcelWriter('陶.xlsx')
data.to_excel(writer, 'shell1',index=False)
writer.save()








