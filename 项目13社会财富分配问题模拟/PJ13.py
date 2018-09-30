# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
# 引用自定义函数
import PJ13_function

# os.chdir('D:\\code\\2018spyder\\项目13社会财富分配问题模拟\\输出')
os.chdir('.\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出')

print('导入模块完成')

# %%设置输出的地址
exportQ1NoSort = ".\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出\\问题1:不允许借贷—不排序"
exportQ1Sort = ".\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出\\问题1:不允许借贷—排序"
exportQ2NoSort = ".\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出\\问题2:允许借贷—不排序"
exportQ2Sort = ".\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出\\问题2:允许借贷—排序"
exportQ3NoSort = ".\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出\\问题3:允许借贷-努力—不排序"
exportQ3Sort = ".\\0code\\spyder_exam\\项目13社会财富分配问题模拟\\输出\\问题3:不允许借贷-努力—排序"
print('设置系统量完成')

# %% 问题1
# 设定初始参数：游戏玩家100人，起始资金100元
person_n = [x for x in range(1, 101)]
fortuneQ1 = pd.DataFrame([100 for i in range(100)], index=person_n)
fortuneQ1.index.name = 'id'
print('初始值设定完成')
# 开始循环
startTime = time.time()
for i in range(1,100):
    fortuneQ1[i] = processQ1(fortuneQ1,i)
resultQ1 = fortuneQ1.T
endTime = time.time()
print('问题一总共运行%i秒'%(endTime-startTime))

print(resultQ1.tail())

# %%问题1绘制柱状图
os.chdir(exportQ1NoSort)

Pic1(resultQ1,0,100,10)
Pic1(resultQ1,100,1000,100)
Pic1(resultQ1,1000,17400,400)

print("'问题1:不允许借贷—不排序'输出完成")

os.chdir(exportQ1Sort)

Pic2(resultQ1,0,100,10)
Pic2(resultQ1,100,1000,100)
Pic2(resultQ1,1000,17400,400)

print("'问题1:不允许借贷—不排序'输出完成")
del exportQ1NoSort,exportQ1Sort
