#!/usr/bin/python
# -*- coding:utf8 -*-

import tensorflow as tf

#train model

print 'train model'

x = tf.placeholder(tf.float32,[None,784]) #输入占位符
y = tf.placeholder(tf.float32,[None,10]) #输入占位符,预期输出
W = tf.Variable(tf.zeros([784,10]));
b = tf.Variable(tf.zeros([10]));
a = tf.nn.softmax(tf.matmul(x,W) + b) #表示模型的实际输出

#定义损失函数和训练方法
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y*tf.log(a), reduction_indices=[1])) #损失函数为交叉熵
optimizer = tf.train.GradientDescentOptimizer(0.5) #梯度下降法，学习速率为0.5
train = optimizer.minimize(cross_entropy);  #训练目标，最小化损失函数

#test model

print 'test model'
correct_prediction = tf.equal(tf.argmax(a,1), tf.argmax(y, 1));
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32));

