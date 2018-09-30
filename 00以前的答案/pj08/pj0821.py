# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False


#D11 = pd.DataFrame()
D11 = pd.concat([Aa,Bb,Cc,Dd])[['id','店名','time','price']]

#del A,B,C,D,E,F,G,cj11,colors,lst_brand,lst_type

D11['日期'] = pd.cut(D11['time'],[4,10,11,14],labels = ['双十一前','双十一当天','双十一后'])
#df[df['date'] == 11]

D110 = D11[['id','price','日期']].groupby(['id','price']).min()
D110.reset_index(inplace = True)
D111 =  D110['id'].value_counts()

D1110 = D111[D111.values == 1]
D1111 = D111[D111.values > 1]

print('真打折的商品数量约占比%.2f%%，不打折的商品数量约占比%.2f%%' %(len(D1111)/len(D111)*100,len(D1110)/len(D111)*100))



print('finsh')

del D111,D1110,D1111

D11b = D110[['price','id']][D110['日期'] == '双十一前']
D11i = D110[['price','id']][D110['日期'] == '双十一当天']

D11zk = pd.merge(D11b,D11i,on = 'id')
D11zk['zkl'] = D11zk['price_y']/D11zk['price_x']*10

D11js = D11zk[D11zk['zkl']<9.5]

#D11js['zkl_range'] = pd.cut(D11js['zkl'],bins = np.linspace(0,9.5,20))
#zuotu01 = D11js.groupby('zkl_range').count()
#zuotu01['zkl_pre'] = zuotu01['zkl']/zuotu01['zkl'].sum()
#zuotu01.reset_index(inplace = True)