# -*- coding: utf-8 -*-

from bokeh.plotting import figure,show,output_file

output_file("D11.html")

from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.core.properties import value
# 导入相关模块

lst_brand = cj11.index.tolist()
lst_type = cj11.columns.tolist()[:2]
colors = ["#718dbf" ,"#e84d60"]
# 设置好参数

cj11.index.name = 'brand'
cj11.columns = ['sale_on_11','presell','sum']
# 修改数据index和columns名字为英文

source = ColumnDataSource(data=cj11)
# 创建数据

hover = HoverTool(tooltips=[("品牌", "@brand"),
                            ("双十一当天参与活动的商品数量", "@sale_on_11"),
                            ("预售商品数量", "@presell"),
                            ("参与双十一活动商品总数", "@sum")
                           ])  # 设置标签显示内容

p = figure(x_range=lst_brand, plot_width=900, plot_height=350, title="各个品牌参与双十一活动的商品数量分布",
          tools=[hover,'reset,xwheel_zoom,pan,crosshair'])
# 构建绘图空间

p.vbar_stack(lst_type,          # 设置堆叠值，这里source中包含了不同年份的值，years变量用于识别不同堆叠层
             x='brand',     # 设置x坐标
             source=source,
             width=0.9, color=colors, alpha = 0.8,legend=[value(x) for x in lst_type],
             muted_color='black', muted_alpha=0.2
             )
# 绘制堆叠图

#p.xgrid.grid_line_color = None
#p.axis.minor_tick_line_color = None
#p.outline_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "vertical"
p.legend.click_policy="mute"
# 设置其他参数

show(p)

#del A,B,C,D,E,F,G,cj11,colors,lst_brand,lst_type