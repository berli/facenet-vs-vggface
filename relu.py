#!/usr/bin/python
#-*- coding: utf-8 -*-)

import tensorflow as tf

#tf.nn.relu(features, name = None)
#解释：这个函数的作用是计算激活函数relu，即max(features, 0)。即将矩阵中每行的非最大值置0。
a = tf.constant([-1, 2.0, 3])
b = tf.nn.relu(a)
sess = tf.Session()
print sess.run(b)
