#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

weight = tf.Variable(1, dtype=tf.float32)
bias   = tf.Variable(-1, dtype=tf.float32)
x = tf.placeholder(tf.float32)
line_regress = weight * x + bias

y = tf.placeholder(tf.float32)


squared_delta = tf.square(line_regress - y)
loss = tf.reduce_sum(squared_delta)

sess = tf.Session()

#optimizer = tf.train.GradientDescentOptimizer(0.01)
optimizer = tf.train.AdamOptimizer(0.01)
train = optimizer.minimize(loss)

sess.run(tf.global_variables_initializer())

with tf.name_scope("weight"):
    tf.summary.histogram("Weight", weight)
with tf.name_scope("bias"):
    tf.summary.histogram("Bias", bias)
with tf.name_scope("loss"):
    tf.summary.histogram("Loss", loss)

summary_op = tf.summary.merge_all()
summary_write = tf.summary.FileWriter('./log/', tf.get_default_graph())

for i in range(1000):
    _,summary = sess.run([train,summary_op], {x:[1,2,3,4], y:[0, -1,-2,-3]})
    if( i % 10 == 0):
        #log_writer = tf.summary.FileWriter('./log/')
        summary_write.add_summary(summary, i);

        print(i, sess.run([weight, bias, loss], {x:[1,2,3,4], y:[0,-1,-2,-3]}))
