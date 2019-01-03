#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf
import numpy

a = tf.Variable(tf.random_normal([10,1]))
b = tf.nn.embedding_lookup(a, [1, 3])

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print('input:',sess.run(a))
    print('embeding:',sess.run(b))
