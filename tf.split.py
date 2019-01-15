
#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

a = tf.Variable(tf.random_normal(shape=[2,6,2]))
s = tf.split(a, 2, 0)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer());
    print 'a:',sess.run(a)
    print 's:',sess.run(s)

