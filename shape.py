#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

t = tf.constant([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]])
l = tf.constant([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
s = tf.shape(t)
s1 = tf.shape(t)[2]

with tf.Session() as sess:
    print (sess.run(s))
    print (sess.run(s1))
    print (sess.run(l))
