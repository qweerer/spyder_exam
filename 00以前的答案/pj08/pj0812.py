import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False




A = Aa.drop_duplicates(subset=['id'],keep='first')
B = Bb.drop_duplicates(subset=['id'],keep='first')
C = Cc.drop_duplicates(subset=['id'],keep='first')
D = Dd.drop_duplicates(subset=['id'],keep='first')
E = Ee.drop_duplicates(subset=['id'],keep='first')
F = Ff.drop_duplicates(subset=['id'],keep='first')
G = Gg.drop_duplicates(subset=['id'],keep='first')

Ea = Ea.drop_duplicates(subset=['id'],keep='first')
Fa = Fa.drop_duplicates(subset=['id'],keep='first')
#Eeb = Eeb.drop_duplicates(subset=['id'],keep='first')

#D11_on = pd.DataFrame()
#D11_on = pd.concat([D11_on,A,B,C,D])
D11_off_num = len(E)+len(F)+len(G)

#cj = pd.concat([F,group])


print('当天未参加活动的商品共%i个，占比%.2f %%'%(D11_off_num,(D11_off_num/allid*100)))
print('未参加活动的商品类别为[E,F,G]')
print('未参见活动的商品中：')
print('暂时下架有%i个，重新上架有%i个，预售商品有%i个'%(len(F),len(D11_on_3),len(Ea)+len(Fa)))


s = pd.Series([len(A),len(C),len(B),len(D),len(E),len(F),len(G)], index=['A', 'C','B','D','E','F','G'], name='series')
from bokeh.palettes import brewer
colori = brewer['GnBu'][7]
plt.axis('equal') 
plt.pie(s,
       labels = s.index,
       colors = colori,
       autopct='%.2f%%',
       pctdistance=0.8,
       shadow = True,
       startangle=90,
       radius=1.5,
       counterclock=False)
print(s)

del s,colori,brewer,allid,D11_on_1,D11_on_2,D11_on_3,D11_off_num,time