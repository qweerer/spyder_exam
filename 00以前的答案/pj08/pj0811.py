# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False

Aa = pd.DataFrame()
Bb = pd.DataFrame()
Cc = pd.DataFrame()
Dd = pd.DataFrame()
Ee = pd.DataFrame()
Ff = pd.DataFrame()
Gg = pd.DataFrame()

#data1 = pd.DataFrame({'time':[5,6,7,8,9],'id' : [1,1,1,1,1]})

for name,group in data.groupby('id'):
    timelist = list(group['time'])
    timeser = group['time']
    if 11  in timelist:
        if (timeser < 11).any():
            if (timeser > 11).any():
                Aa = pd.concat([Aa,group])
            else :
                Bb = pd.concat([Bb,group])
        elif (timeser > 11).any():
            Cc = pd.concat([Cc,group])
        else:
            Dd = pd.concat([Dd,group])
    elif (timeser < 11).any():
        if (timeser > 11).any():
            Ff = pd.concat([Ff,group])
        else:
            Ee = pd.concat([Ee,group])
    else:
        Gg = pd.concat([Gg,group])
            
del timelist,timeser,name,group

#ok = data.head()['update_time'].tolist
Ea = Ee[Ee['title'].str.contains('预售')]
Fa = Ff[Ff['title'].str.contains('预售')]

#D11_on = pd.DataFrame()
#D11_on = pd.concat([D11_on,A,B,C,D])

D11_on_1 = pd.concat([Cc,Dd,Ee])
D11_on_1 = D11_on_1[['title','id','time']].groupby(by = ['id','title']).count()
D11_on_1 = D11_on_1.reset_index()['id'].value_counts()
D11_on_1 = D11_on_1[D11_on_1>1]

D11_on_2 = pd.concat([Cc,Dd,Ff])
D11_on_2 = D11_on_2[['title','id','time']].groupby(by = ['id','title']).count()
D11_on_2 = D11_on_2.reset_index()['id'].value_counts()
D11_on_2 = D11_on_2[D11_on_2>1]

D11_on_3 = pd.concat([D11_on_1,D11_on_2])
#D11_on_3.groupby(D11_on_3.index).count()

