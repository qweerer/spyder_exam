# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False


zuotu31 = data.drop_duplicates(subset=['id'],keep='first')
zuotu31 = zuotu31[['店名','id']].groupby('店名').count()
zuotu32 = zuotu13[['店名','zkl']].groupby('店名').mean()
zuotu33 = zuotu13[['店名','id']].groupby('店名').count()

zuotu32['zkl'] = zuotu32['zkl']*0.1
zuotu31.columns = ['allitem']
zuotu33.columns = ['offitem']

zuotu31 = pd.merge(zuotu31,zuotu32,left_index=True,right_index=True)
zuotu31 = pd.merge(zuotu31,zuotu33,left_index=True,right_index=True)

zuotu31['off_all'] = zuotu31['offitem']/zuotu31['allitem']
zuotu31['size'] = zuotu31['allitem']*0.2
zuotu31.index.name = 'index'


from bokeh.plotting import figure,show,output_file

output_file("D114.html")

from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.core.properties import value
from bokeh.transform import jitter

from bokeh.models.annotations import Span            # 导入Span模块
from bokeh.models.annotations import Label           # 导入Label模块
from bokeh.models.annotations import BoxAnnotation   # 导入BoxAnnotation模块

source = ColumnDataSource(zuotu31)

x_mean = zuotu31['off_all'].mean()
y_mean = zuotu31['zkl'].mean()

hover = HoverTool(tooltips=[("品牌", "@index"),
                            ("折扣率", "@zkl"),
                            ("商品总数", "@allitem"),
                            ("参与打折商品比例", "@off_all")])

p4 = figure(plot_width = 800,plot_height = 800,title = "双11美妆产品品牌套路",
            tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair'])
p4.circle_x(x = 'off_all',y = 'zkl',size = 'size',source = source,
          color = 'red',alpha =0.7,
          line_color = 'black',line_dash = [8,4],line_width =2)

x = Span(location=x_mean, dimension='height', line_color='green',line_alpha = 0.7, line_width=1.5, line_dash = [6,4])
y = Span(location=y_mean, dimension='width', line_color='green',line_alpha = 0.7, line_width=1.5, line_dash = [6,4])
p4.add_layout(x)
p4.add_layout(y)
# 绘制辅助线

bg1 = BoxAnnotation(bottom=y_mean, right=x_mean,fill_alpha=0.1, fill_color='olive')
label1 = Label(x=0.1, y=0.45,text="少量大打折",text_font_size="10pt" )
p4.add_layout(bg1)
p4.add_layout(label1)
# 绘制第一象限

bg2 = BoxAnnotation(bottom=y_mean, left=x_mean,fill_alpha=0.1, fill_color='firebrick')
label2 = Label(x=0.5, y=0.45,text="大量大打折",text_font_size="10pt" )
p4.add_layout(bg2)
p4.add_layout(label2)
# 绘制第二象限

bg3 = BoxAnnotation(top=y_mean, right=x_mean,fill_alpha=0.1, fill_color='firebrick')
label3 = Label(x=0.1, y=0.80,text="少量少打折",text_font_size="10pt" )
p4.add_layout(bg3)
p4.add_layout(label3)
# 绘制第三象限

bg4 = BoxAnnotation(top=y_mean, left=x_mean,fill_alpha=0.1, fill_color='olive')
label4 = Label(x=0.5, y=0.80,text="少量大打折",text_font_size="10pt" )
p4.add_layout(bg4)
p4.add_layout(label4)
show(p4)








