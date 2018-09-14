import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_excel('双十一淘宝美妆数据.xlsx',sheetname = 0)
# 删除赠品
data = data[data['price'] > 5]
data = data[data !=0].dropna()
data.index = data['update_time']
data['time'] = data.index.day
#print(data.head())

time =  data['time'].unique()
name = data['店名'].unique()
allid = len(data.groupby('id').count())
print('本次共采集数据：%i 条'%(allid))
print('涉及到%i个店铺'%(len(name)))
print(name)
