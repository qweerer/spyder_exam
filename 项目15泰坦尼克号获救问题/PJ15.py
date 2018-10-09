# -*- coding: utf-8 -*-
# %%
import os
import time

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pylab import mpl

# 导入图表绘制、图标展示模块
# output_file → 非notebook中创建绘图空间

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

os.chdir('D:/user/Documents/00code/spyder_exam/项目15泰坦尼克号获救问题/输出')
# os.chdir('/home/qweerer/0code/spyder_exam/项目15泰坦尼克号获救问题')

# pathPj14 = os.path.abspath('.')
print('导入模块完成')

#################################
# %%问题1
