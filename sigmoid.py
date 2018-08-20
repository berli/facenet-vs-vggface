#!/usr/bin/python #encoding:utf-8
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus']=False
 
 
def  sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
 
fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
 
x = np.linspace(-10, 10)
y = sigmoid(x)
tanh = 2*sigmoid(2*x) - 1
 
plt.xlim(-11,11)
plt.ylim(-1.1,1.1)
 
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

#设置x轴刻度
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.set_xticks([-10,-9,-7,-5,-3,-1,0,1,3,5,7,9,10])

#设置y轴刻度
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
ax.set_yticks([-1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1])
 
plt.plot(x,y,label="Sigmoid",color = "red")
#plt.plot(2*x,tanh,label="Tanh", color = "blue")
plt.legend()
plt.show()

