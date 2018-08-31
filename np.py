#!/usr/bin/python
#-*- coding: utf-8 -*-)

import numpy as np

a = np.array([1,2,3])
print a
#一维数组的平均值
m = np.mean(a)
print 'm:',m

a2 = np.array([[1,2,3],[4,5,6]])
print a2
#对所有元素求平均值
#(1+2+3+4+5+6)/6
m2 = np.mean(a2)
print '所有元素平均值:',m2

#每一列求平均值
m30 = np.mean(a2, axis=0)
print 'axis=0每一列平均值:',m30

#每一列求平均值
m31 = np.mean(a2, axis=1)
print 'axis=1每一行平均值:',m31
