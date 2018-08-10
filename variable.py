# -*- coding: utf8 -*-
import tensorflow as tf

v1 = tf.Variable(tf.random_normal([3,2], stddev=1, seed=1, dtype=tf.float32, name="v1"))
v2 = tf.get_variable(name="v", shape=[2,2], initializer= tf.zeros_initializer)
w1 = tf.constant([[1,2,3],[4,5,6]])

sess = tf.Session()
sess.run(tf.global_variables_initializer())

print sess.run(v1)
print sess.run(v2)
print sess.run(w1)

