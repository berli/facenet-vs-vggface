# -*- coding: utf-8 -*-
import tensorflow as tf

a = [1.0,2.0,3.0,4.0]
b = [0.3,0.1,0.0]

with tf.Session() as sess:
    print(sess.run(tf.nn.softmax(a)))
    print(sess.run(tf.nn.softmax(b)))
