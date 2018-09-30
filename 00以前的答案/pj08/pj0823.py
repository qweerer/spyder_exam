# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False


from bokeh.plotting import figure,show,output_file

output_file("D113.html")

from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.core.properties import value
from bokeh.transform import jitter

zuotu13 = data[['id','店名']].drop_duplicates(subset=['id'],keep='first')


zuotu13 = pd.merge(zuotu13,D11js[['id','zkl']],on='id')
zuotu13.index.name = 'index'


# 创建数据
brands =zuotu13['店名'].dropna().unique().tolist()   #Y轴
source2 = ColumnDataSource(data = zuotu13)
hover = HoverTool(tooltips=[("折扣率", "@zkl"+'折')])  # 设置标签显示内容


p3 = figure(plot_width=800, plot_height=600,title="不同品牌折扣率情况",y_range = brands,
            tools = [hover,'reset,xwheel_zoom,pan,crosshair'])

p3.circle(x='zkl', 
          y=jitter('店名', width=0.6, range=p3.y_range),
          source=source2,alpha = 0.6,color = 'green')
# jitter参数 → 'day'：第一参数，这里指y的值，width：间隔宽度比例，range：分类范围对象，这里和y轴的分类一致

#p3.ygrid.grid_line_color = None
# 设置其他参数

show(p3)




