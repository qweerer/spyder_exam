# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid",{"font.sans-serif":['simhei','Droid Sans Fallback']})
plt.rcParams['axes.unicode_minus'] = False

#data = pd.DataFrame()

data_th = data[['类别','口味','环境','服务','人均消费','点评数']][data !=0].dropna()
data_th['营业额'] = data_th['人均消费']*data_th['点评数']
s = data_th['营业额'].describe()
q1 = s['25%']
q3 = s['75%']

data_th['加权'] = 0
data_th['加权'].loc[data_th['营业额']>=q3] = 3
data_th['加权'].loc[data_th['营业额']<q3] = 2
data_th['加权'].loc[data_th['营业额']<q1] = 1


data_th['性价比'] = (data_th['口味']+data_th['环境']+data_th['服务'])/data_th['人均消费'] *data_th['加权']

data_th2 = data_th[['类别','口味','人均消费','性价比']]
#del data_th

#####################################################
# 异常值处理
#定义删除异常值的函数
def deldif (df,col):    
    s = df[col].describe()        
    q1 = s['25%']
    q3 = s['75%']
    iqr = q3 - q1
    mi = q1 - 1.5*iqr
    ma = q3 + 1.5*iqr
    #df_c = pd.DataFrame()
    df_c = df[(df[col] >= mi) & (df[col] <= ma)]
    return df_c


#批量删除异常值
def data_del (df,*cols):
    data_gby = {}
    data_re = pd.DataFrame()


    for name,group in df.groupby('类别'):
        data_gby.update({name:group})
        
    for name in data_gby:
        for col in cols:
            data_gby[name] = deldif(data_gby[name],col)
        
        data_re = pd.concat([data_re,data_gby[name]])
            
    return data_re      
    
    
    
data_th2 = data_del(data_th2,'口味','人均消费','性价比')
#########################################################
# 标准化处理

def zero_one (df, *cols):
    df_n = df.copy()
    for col in cols:
        ma = df_n[col].max()
        mi = df_n[col].min()
        df_n[col + '得分'] = (df_n[col] - mi) / (ma - mi)
    return(df_n)

data_th3 = data_th2.groupby('类别').mean()

# 因为人均消费是'价格适中即可',所以这里将'人均消费'-'均值',得到'人均消费与均值的差距',越小越好
meanmoney = data_th3['人均消费'].mean()
data_th3['人均消费_'] = abs(data_th3['人均消费']-meanmoney)

data_th4 = zero_one(data_th3,'口味','人均消费_','性价比')

#因为上边得到的'人均消费与均值的差距',越小越好,但在统一化处理中是越大越好的处理,所以,1-'人均消费'得到最后的值
data_th4['人均消费_得分'] = 1-data_th4['人均消费_得分']
del data_th2, data_th3,meanmoney
########################################################



    
    
    
    
    
    
    
    
    
    
    