# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False


data_th5 = data_th4.copy()
data_th5['size'] = data_th4['口味得分']*30

from bokeh.plotting import figure,show,output_file

output_file("line.html")

from bokeh.models import HoverTool
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.annotations import BoxAnnotation

data_th5.index.name = 'type'
data_th5.columns = ['kw','price','xjb','price_','kw_norm','price_norm','xjb_norm','size']
source = ColumnDataSource(data_th5)


hover = HoverTool(tooltips=[("餐饮类型", "@type"),
                            ("人均消费", "@price"),
                            ("性价比得分", "@xjb_norm"),
                            ("口味得分", "@kw_norm")
                           ])  # 设置标签显示内容




s1 = figure(plot_width=800, plot_height=250, title='餐饮类型得分情况',
            x_axis_label = '人均消费', y_axis_label = '性价比得分', 
            tools=[hover,'box_select,lasso_select,reset,xwheel_zoom,pan,crosshair'])
s1.circle(x = 'price', y = 'xjb_norm',size = 'size',source = source, color="navy", alpha=0.5)
center = BoxAnnotation(left=40, right=100,  # 设置矩形四边位置
                       fill_alpha=0.1, fill_color='gray'        # 设置透明度、颜色
                      )
s1.add_layout(center)
# 散点图

rangename = data_th5.index.tolist()
s2 = figure(plot_width=800, plot_height=250, title='口味得分',
            x_range = rangename)
s2.vbar(x='type', width=0.9, bottom=0,top='kw_norm', source = source, 
       line_width = 1,line_alpha = 0.8,line_color = 'black', line_dash = [5,2],    # 单独设置线参数
       fill_color = 'red',fill_alpha = 0.6    # 单独设置填充颜色参数
      )
#s2.xaxis.major_label_orientation = 'vertical'
#s2.xaxis.major_label_text_baseline = 'bottom'
# 直方图1

s3 = figure(plot_width=800, plot_height=250, title='人均消费得分',
            x_range = rangename)
s3.vbar(x='type', width=0.9, bottom=0,top='price_norm', source = source, 
       line_width = 1,line_alpha = 0.8,line_color = 'black', line_dash = [5,2],    # 单独设置线参数
       fill_color = 'green',fill_alpha = 0.6    # 单独设置填充颜色参数
      )
# 直方图2

p = gridplot([[s1],[s2],[s3]])
#p = gridplot([[s1, s2, s3]])
#p = gridplot([[s1, s2], [None, s3]])
# 组合图表

show(p)





