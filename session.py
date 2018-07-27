#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf
import time as t

x = tf.Variable([1.0])
b = 1.0

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    s1 = t.time()
    #通过step run的方式读取变量
    for i in range(100000):
        res = sess.run(x)
    print "通过sess.run读取变量的时间:",t.time() - s1

    s2 = t.time()
    for i in range(100000):
        a = b
    print "通过直接赋值的时间:", t.time() - s2


