#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf
from numpy.random import RandomState

#定义batch训练大小
batch_size = 8

#在shape上使用None表示维度的具体数值不确定
x = tf.placeholder(tf.float32, shape=[None, 2], name='x-input')
y_ = tf.placeholder(tf.float32, shape=[None, 1], name='y-input')

#定义神经网络的参数
w1 = tf.Variable(tf.random_normal([2,3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3,1], stddev=1, seed=1))
bias1 = tf.Variable(tf.random_normal([3], stddev=1, seed=1))
bias2 = tf.Variable(tf.random_normal([1], stddev=1, seed=1))

#定义神经网络前向传播过程
a = tf.nn.relu(tf.matmul(x, w1)+bias1)
y = tf.nn.relu(tf.matmul(a, w2)+bias2)

#定义损失函数和前向传播算法
loss = tf.reduce_sum(tf.pow((y-y_), 2))

#梯度下降优化算法
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

#用随机数产生一个数据集
#seed = 1每次产生的随机数都一样
rdm = RandomState(seed = 1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)
Y = [[x1 + 10*x2] for (x1, x2) in X]

with tf.Session() as sess:

    #定义命名空间，使用tensorboard进行可视化
    with tf.name_scope("inputs"):
        tf.summary.histogram('X', X)

    with tf.name_scope("target"):
        tf.summary.histogram('Target', Y)

    with tf.name_scope("outpus"):
        tf.summary.histogram('Y', y)

    with tf.name_scope("loss"):
        tf.summary.histogram('Loss', loss)

    summary_op = tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter('./log/', tf.get_default_graph())
    
    #初始化变量
    sess.run(tf.global_variables_initializer())
    
    STEPS = 10000
    for i in range(STEPS + 1):
        #每次选取batchsize个样本进行训练
        start = (i*batch_size) % dataset_size;
        end = min(start + batch_size, dataset_size);
    
        #通过选取的样本更新神经网络并更新参数
        sess.run(train_step, feed_dict={x: X[start:end], y_:Y[start:end]})
        if(i % 500 == 0):
            #每隔一段时间计算所有数据上的loss并输出
            total_cross_entry, summary = sess.run([loss, summary_op], feed_dict={x:X, y_:Y})
            print("After %d training steps, loss is on all data is %g" % (i, total_cross_entry))
    
            #训练结束后，输出神经网络的参数
    
            log_writer = tf.summary.FileWriter('./log/')
            log_writer.add_summary(summary, i)

    print sess.run(w1)
    print sess.run(w2)
