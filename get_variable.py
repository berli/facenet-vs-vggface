#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

g1 = tf.Graph()
with g1.as_default():
    #g1是默认计算图,在计算图g1中定义变量"v",初始值为0
    # W = tf.get_variable(name, shape=None, dtype=tf.float32, initializer=None,
    #       regularizer=None, trainable=True, collections=None)
    v = tf.get_variable("v", shape=[1], initializer=tf.zeros_initializer);

g2 = tf.Graph()
with g2.as_default():
    v = tf.get_variable("v", shape=[1], initializer=tf.ones_initializer)

#在计算图g1中读取变量g1的值
with tf.Session(graph=g1) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse = True):
        print (sess.run(tf.get_variable("v")))

with tf.Session(graph = g2) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse = True):
        print (sess.run(tf.get_variable("v")))
