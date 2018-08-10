'''''******************************************************************
    > File Name: shape.py
    > Author: berli
    > Mail: berli@tencent.com 
    > Created Time: 2018年08月10日 星期五 16时22分29秒
 *****************************************************************'''

#!/usr/bin/python
# -*- coding: utf8 -*-)

import tensorflow as tf

t = tf.constant([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]])
s = tf.shape(t)

with tf.Session() as sess:
    print (sess.run(s))
