#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

#生成一个FIFO队列和QueueRunner
file = ['queue_test.csv']
file_queue = tf.train.string_input_producer(file, shuffle = False)

#定义Reader
reader = tf.TextLineReader()
key, value = reader.read(file_queue)

#定义解析器
record_defaults = [[0.0] for col in range(8)]
print 'record_defaults =',record_defaults
line = tf.decode_csv(value, record_defaults = record_defaults)
print('line = ', line)

with tf.Session() as sess:
    #创建一个协调器，管理线程
    coord = tf.train.Coordinator()
    #启动Queue,文件名已经进入队列
    threads = tf.train.start_queue_runners(coord=coord)

    sess.run(tf.global_variables_initializer())
    for i in range(10):
        print sess.run(line)
    
    coord.request_stop()
    coord.join(threads)

