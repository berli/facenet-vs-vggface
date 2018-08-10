#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

weight = tf.Variable(3, dtype = tf.float32)
bias   = tf.Variable(1, dtype = tf.float32)
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)

line_gress = weight * x + bias

sess = tf.Session()
sess.run(tf.global_variables_initializer())

squared_delta = tf.square(line_gress - y)
loss = tf.reduce_sum(squared_delta)

print "line_gress:", sess.run(line_gress, {x:[1,2,3,4], y:[0,-1,-2,-3]})
print "y:", sess.run(y, {y:[0,-1,-2,-3]})
print "line_gress - y:", sess.run(line_gress-y, {x:[1,2,3,4], y:[0,-1,-2,-3]})
print "loss:", sess.run(loss, {x:[1,2,3,4], y:[0,-1,-2,-3]})

fixw = tf.assign(weight, -1)
fixb = tf.assign(bias, 1.)

print 'assign:', sess.run([fixw, fixb])
