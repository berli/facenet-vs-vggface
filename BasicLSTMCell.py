#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

batch_size = 4
input = tf.random_normal(shape=[3, batch_size, 6], dtype=tf.float32)
cell = tf.nn.rnn_cell.BasicLSTMCell(10, forget_bias = 1.0, state_is_tuple = True)
init_state = cell.zero_state(batch_size, dtype = tf.float32)
out_put, final_state = tf.nn.dynamic_rnn(cell, input, initial_state=init_state, time_major = True)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print (sess.run(out_put))
    print (sess.run(final_state))
