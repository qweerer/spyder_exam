# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False


data2 = pd.read_excel('qgis导出.xlsx',sheetname = 'Sheet1')

data2.fillna(0,inplace = True)
data2.columns = ['人口密度','道路长度','餐饮统计','疆菜餐饮统计','lng','lat']


# 表转化
def zero_one (df, *cols):
    df_n = df.copy()
    for col in cols:
        ma = df_n[col].max()
        mi = df_n[col].min()
        df_n[col + '_norm'] = (df_n[col] - mi) / (ma - mi)
    return(df_n)

data2_norm = zero_one(data2,'人口密度','餐饮统计','疆菜餐饮统计','道路长度')

data2_norm['疆菜餐饮统计_norm'] = 1 - data2_norm['疆菜餐饮统计_norm']
data2_norm['final_score'] = data2_norm['人口密度_norm']*0.4 + data2_norm['餐饮统计_norm']*0.3 + data2_norm['疆菜餐饮统计_norm']*0.1 + data2_norm['道路长度_norm']*0.2
data2_norm = data2_norm.sort_values(by = 'final_score',ascending = False).reset_index()

from bokeh.plotting import figure,show,output_file

output_file("上海地图.html")

from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

data2_norm['size'] = data2_norm['final_score'] * 15
data2_norm['color'] = 'green'
data2_norm['color'].iloc[:10] = 'red'
# 添加size字段

source = ColumnDataSource(data2_norm)
# 创建ColumnDataSource数据

hover = HoverTool(tooltips=[("经度", "@lng"),
                            ("纬度", "@lat"),
                            ("最终得分", "@final_score"),
                           ])  # 设置标签显示内容
p = figure(plot_width=800, plot_height=800,
           title="空间散点图" , 
           tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair']) 
# 构建绘图空间

p.circle(x = 'lng',y = 'lat',size = 'size',source = source,
         color="color",alpha=0.5,line_color = 'black')
show(p)


