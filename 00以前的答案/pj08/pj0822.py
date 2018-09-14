# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False


from bokeh.plotting import figure,show,output_file

output_file("D112.html")

from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.core.properties import value
# 导入相关模块
#D11js['zkl_range'] = pd.cut(D11js['zkl'],bins = np.linspace(0,9.5,20))
#zuotu01 = D11js.groupby('zkl_range').count()
#zuotu01['zkl_pre'] = zuotu01['zkl']/zuotu01['zkl'].sum()
#zuotu01.reset_index(inplace = True)

zuotu11 = D11js[['id','zkl']]
d2 = [c/2 for c in list(range(20)[1:])]
zuotu11['zkl_range'] = pd.cut(zuotu11['zkl'],list(np.linspace(0,9.5,20)),labels = d2)
zuotu11 = zuotu11.groupby('zkl_range').count()
zuotu11.index.name = 'index'
#zuotu12 = zuotu11.reset_index()
#zuotu12['zkl_range'].astype(np.str)

zuotu12 = D11js[['id','zkl']]
#zuotu12['zkl_range'] = pd.cut(zuotu11['zkl'],bins = np.linspace(0,10,11))
zuotu12['zkl_range'] = pd.cut(zuotu12['zkl'],list(np.linspace(0,9.5,20)))
zuotu12 = zuotu12.groupby('zkl_range').count()
zuotu12.reset_index(inplace = True)
lst_brand = zuotu12['zkl_range'].astype(np.str).tolist()
#lst_brand = d2.astype(np.str).tolist()

p2 = figure()

hover = HoverTool(tooltips = [('商品数量','@zkl'+'个')])
source = ColumnDataSource(data = zuotu11)

p2 = figure(plot_width=600, plot_height=400,title="商品折扣率统计",x_range=lst_brand,
            tools = [hover,'reset,xwheel_zoom,pan,crosshair'])
p2.line(x = 'index',y='id',source = source,     
        line_width=3, line_alpha = 0.8, line_color = 'red')   # 线型基本设置
p2.circle(x = 'index',y='id',source = source, size = 10,color = 'orange',alpha = 0.8)

show(p2)
# del zuotu11,zuotu12,D110,D11b,D11i,lst_brand,d2