# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False



cj11_y = pd.concat([A,B,C,D])
cj11_ys = pd.concat([Ea,Fa])

cj11_y = cj11_y[['店名','time']].groupby('店名').count()
cj11_ys= cj11_ys[['店名','time']].groupby('店名').count()
cj11_y.rename(columns={'time':'双11当天在售的商品'},inplace=True)
cj11_ys.rename(columns={'time':'预售的商品'},inplace=True)
cj11 = pd.merge(cj11_y,cj11_ys,left_index=True,right_index=True)

cj11['参与双十一活动商品总数'] = cj11['双11当天在售的商品'] + cj11['预售的商品']

del cj11_y,cj11_ys,Fa,Ea