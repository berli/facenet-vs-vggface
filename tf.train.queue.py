#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

# 生成一个先入先出队列和一个QueueRunner
filenames = ['A.csv', 'B.csv', 'C.csv']
filename_queue = tf.train.string_input_producer(filenames, shuffle=False)

# 定义Reader
reader = tf.TextLineReader()
key, value = reader.read(filename_queue)

# 定义Decoder
example, label = tf.decode_csv(value, record_defaults=[['null'], ['null']])
print 'example =', example
print 'label = ', label
# 运行Graph
with tf.Session() as sess:
    coord = tf.train.Coordinator()  #创建一个协调器，管理线程
    threads = tf.train.start_queue_runners(coord=coord)  #启动QueueRunner, 此时文件名队列已经进队。
    for i in range(10):
        print example.eval()   #取样本的时候，一个Reader先从文件名队列中取出文件名，读出数据，Decoder解析后进入样本队列。
    coord.request_stop()
    coord.join(threads)
