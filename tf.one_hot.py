#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

size = 6
depth = 8

label = tf.constant([0,1,2,3,4,5,6,7])
#转换到one-hot编码，对就一个函数搞定
one_hot = tf.one_hot(indices = label, depth=depth)
print 'one_hot type=',type(one_hot)
with tf.Session() as sess:
    #sess.run(tf.global_variables_initializer())
    print 'label =', sess.run(label)
    print 'one_hot =',sess.run(one_hot)
    #把tensor转为numpy 数组
    #两种写法都可以
    #np_array = one_hot.eval(session=sess)
    np_array = sess.run(one_hot)
    print 'numpy =', np_array[1]
    print 'type =', type(np_array)

