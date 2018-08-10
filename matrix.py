#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

w1 = tf.Variable(tf.random_normal([3, 2], stddev=1, seed = 1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev = 1, seed = 1))

x = tf.placeholder(shape=[3,2], dtype=tf.float32, name="input")

a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

print "w1\n", sess.run(w1)
print "w2\n", sess.run(w2)
print "x\n", sess.run(x, feed_dict={x:[[0.7, 0.9], [0.1, 0.4], [0.5, 0.8]]})
print "a = x*w1\n", sess.run(a, feed_dict={x:[[0.7, 0.9], [0.1, 0.4], [0.5, 0.8]]})
print "matrix = a *w2\n", sess.run(y, feed_dict={x:[[0.7, 0.9], [0.1, 0.4], [0.5, 0.8]]})
