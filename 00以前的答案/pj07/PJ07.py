# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 11:15:43 2018

@author: liu14
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.char('D:\\user\\Documents\\00Py学习\\spyder\\ch7 pj07')
# % matplotlib inline

data = pd.read_excel('上海餐饮数据.xlsx',sheetname = 'Sheet1')

data = data[data['类别'].notnull()]
data = data[data['点评数']>30]
print(data.head())