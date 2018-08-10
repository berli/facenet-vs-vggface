#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

v1 = tf.Variable(tf.random_normal([2,3], stddev=1,mean=1), dtype=tf.float32)
v2 = tf.Variable(v1.initialized_value())
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print (sess.run(v1))
    
    print "v2\n\n", (sess.run(v2))

