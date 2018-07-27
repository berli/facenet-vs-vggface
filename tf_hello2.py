#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf
 
# 声明占位变量x、y, 形状为[2,2]
x = tf.placeholder("float",shape=[2,2])
y = tf.placeholder("float",[2,2])
 
# 声明变量
W = tf.Variable(tf.zeros([2,2]))
b = tf.Variable(tf.zeros([1]))
 
# 操作
result = tf.matmul(x,W) +b
 
# 损失函数
lost = tf.reduce_sum(tf.pow((y-result),2))
 
# 优化
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(lost)
 
 
with tf.Session() as sess:
    # 初始化变量
    sess.run(tf.global_variables_initializer())
 
    # 这里x、y给固定的值
    x_s = [[1.0, 3.0], [3.2, 4.]]
    y_s = [[6.0, 3.0], [5.2, 43.]]
 
    step = 0
    while(True):
        step += 1
        feed = {x: x_s, y: y_s}
 
        # 通过sess.run执行优化
        sess.run(train_step, feed_dict=feed)
 
        if step % 500 == 0:
            print 'step: {0},  loss: {1}'.format(step, sess.run(lost, feed_dict=feed))
            if sess.run(lost, feed_dict=feed) < 0.00001 or step > 10000:
                print ''
                print 'final loss is: {}'.format(sess.run(lost, feed_dict=feed))
                print("W : {}".format(sess.run(W)))
                print("b : {}".format( sess.run(b)))
 
                result1 = tf.matmul(x_s, W) + b
                print 'final result is: {}'.format(sess.run(result1))
                print 'final error is: {}'.format(sess.run(result1)-y_s)
 
                break

