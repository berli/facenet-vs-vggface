#!/usr/bin/python
#-*- coding: utf-8 -*-)

import tensorflow as tf

#声明占位变量x,y
x = tf.placeholder(tf.float32, shape=[None, 1])
y = tf.placeholder(tf.float32, [None, 1])

#声明变量
w = tf.Variable(tf.zeros([1,1]))
b = tf.Variable(tf.zeros([1]))

#操作
result = tf.matmul(x, w) + b

#损失函数
lost = tf.reduce_sum(tf.pow((result-y), 2))

#优化
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(lost)

with tf.Session() as sess:
    #初始化变量
    sess.run(tf.global_variables_initializer());

    #x,y固定值
    x_s = [[3.0]]
    y_s = [[100.0]]

    step = 0;
    while(True):
        step += 1
        feed_dict={x:x_s, y:y_s}

        #通过sess.run执行初始化
        sess.run(train_step, feed_dict);
        print 'step:{0}, loss:{1}'.format(step, sess.run(lost, feed_dict))
        print 'w: %f' %sess.run(w)
        print 'b: %f' %sess.run(b)
        if( step % 20 == 0):
            print 'step:{0}, loss:{1}'.format(step, sess.run(lost, feed_dict))
            print 'w: %f' %sess.run(w)
            print 'b: %f' %sess.run(b)
            if(sess.run(lost, feed_dict) < 0.00001 or step > 3000):
                print ' '
                print 'final loss is:{}'.format(sess.run(lost, feed_dict))
                print 'final result of {0} = {1}'.format('x*w +b ', 3.0*sess.run(w) + sess.run(b))
                print 'w: %f' %sess.run(w)
                print 'b: %f' %sess.run(b)
                break;
