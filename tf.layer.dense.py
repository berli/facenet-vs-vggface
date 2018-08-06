#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

batch_size = 5
ones = tf.ones([batch_size, 20])
logits = tf.layers.dense(ones, 10)
print (logits.get_shape())

ones = tf.ones([batch_size, 8, 20])
logits = tf.layers.dense(ones, 10)
print (logits.get_shape())

ones = tf.ones([batch_size,6, 8, 20])
print "ones:", ones
logits = tf.layers.dense(ones, 10)
print (logits.get_shape())

