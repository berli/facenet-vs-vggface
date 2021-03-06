# -*- coding: utf-8 -*-)
import tensorflow as tf
import numpy as np

print('----------example 1----------------')
# 定义一个矩阵a，表示需要被卷积的矩阵。
a = np.array(np.arange(1, 1 + 20).reshape([1, 10, 2]), dtype=np.float32)
print('a',a)
print('---------------------------')
# 卷积核，此处卷积核的数目为1
kernel = np.array(np.arange(1, 1 + 4), dtype=np.float32).reshape([2, 2, 1])
print('kernel',kernel)

# 进行conv1d卷积
#conv1d = tf.nn.conv1d(a, kernel, 1, 'VALID')
conv1d = tf.nn.conv1d(value = a, filters =  kernel, stride = 1, padding = 'SAME')

with tf.Session() as sess:
    # 初始化
    tf.global_variables_initializer().run()
    # 输出卷积值
    print(sess.run(conv1d))

print('----------example 2----------------')
time_step = 144
input_size = 14
b = np.array(np.arange(1, 1 + 2016).reshape([1, time_step, input_size]), dtype=np.float32)
# 定义一个序列。

# 进行conv1d卷积
print('b',b)
#conv1d = tf.nn.conv1d(a, kernel, 1, 'VALID')
input_b = tf.placeholder(tf.float32, [None, time_step, input_size])
conv1d = tf.layers.conv1d(inputs = input_b, filters = 2, kernel_size = 3, strides = 2, padding = 'same', activation = tf.nn.relu)
conv2d = tf.layers.conv1d(inputs = conv1d, filters = 4, kernel_size = 3, strides = 2, padding = 'same', activation = tf.nn.relu)
conv4d = tf.layers.conv1d(inputs = conv2d, filters = 8, kernel_size = 3, strides = 2, padding = 'same', activation = tf.nn.relu)
conv8d = tf.layers.conv1d(inputs = conv4d, filters = 16, kernel_size = 3, strides = 2, padding = 'same', activation = tf.nn.relu)
#conv1d = tf.layers.conv1d(inputs = input_b, filters = 1, kernel_size = 3, strides = 2, padding = 'same')
with tf.Session() as sess:
    # 初始化
    tf.global_variables_initializer().run()
    # 输出卷积值
    print(sess.run(conv8d, feed_dict = {input_b:b}))

print('----------example 3----------------')

# (batch, 128, 9) -> (batch, 32, 18)
conv1 = tf.layers.conv1d(inputs=input_b, filters=18, kernel_size=2, strides=1,
    padding='same', activation = tf.nn.relu)

# (batch, 32, 18) -> (batch, 8, 36)
conv2 = tf.layers.conv1d(inputs=conv1, filters=36, kernel_size=2, strides=1,
padding='same', activation = tf.nn.relu)

# (batch, 8, 36) -> (batch, 2, 72)
conv3 = tf.layers.conv1d(inputs=conv2, filters=72, kernel_size=2, strides=1,
padding='same', activation = tf.nn.relu)

with tf.Session() as sess:
    # 初始化
    tf.global_variables_initializer().run()
    # 输出卷积值
    print(sess.run(conv3, feed_dict = {input_b:b}))

print('---------- example 4 max pool ----------------')

time_step = 2016
time_step = 576
input_size = 1
b = np.array(np.arange(1, 1 + time_step).reshape([1, time_step, input_size]), dtype=np.float32)
input_b = tf.placeholder(tf.float32, [None, time_step, input_size])

def conv3_pool(filters=36, kernel_size=2, strides=1):
    # (batch, 128, 9) -> (batch, 32, 36)
    conv1 = tf.layers.conv1d(inputs=input_b, filters=36, kernel_size=kernel_size, strides=strides,
        padding='same', activation = tf.nn.relu)
    max_pool_1 = tf.layers.max_pooling1d(inputs=conv1, pool_size=4, strides=4, padding='same')
    
    # (batch, 32, 18) -> (batch, 8, 72)
    conv2 = tf.layers.conv1d(inputs=max_pool_1, filters=72, kernel_size=kernel_size, strides=strides,
    padding='same', activation = tf.nn.relu)
    max_pool_2 = tf.layers.max_pooling1d(inputs=conv2, pool_size=4, strides=4, padding='same')
    
    # (batch, 8, 36) -> (batch, 2, 144)
    conv3 = tf.layers.conv1d(inputs=max_pool_2, filters=144, kernel_size=kernel_size, strides=strides,
    padding='same', activation = tf.nn.relu)
    max_pool_3 = tf.layers.max_pooling1d(inputs=conv3, pool_size=4, strides=4, padding='same')
    
    print 'max_pool_3',max_pool_3
    lstm = tf.reshape(max_pool_3, [-1, 1])
    with tf.Session() as sess:
        # 初始化
        tf.global_variables_initializer().run()
        # 输出卷积值
        conv = sess.run(max_pool_3, feed_dict = {input_b:b})
        #conv = sess.run(lstm, feed_dict = {input_b:b})
        #print(conv)
        print('len(conv):', np.size(conv))
    
conv3_pool(filters=36, kernel_size=3, strides=2)
print('---------- ----------------')
conv3_pool(filters=36, kernel_size=4, strides=2)
print('---------- ----------------')
conv3_pool(filters=8, kernel_size=3, strides=2)

print('---------- example 5 max pool ----------------')

def conv4_pool(filters=18, kernel_size=2, strides=1):
    # (batch, 128, 9) --> (batch, 64, 18)
    conv1 = tf.layers.conv1d(inputs=input_b, filters=filters, kernel_size=kernel_size, strides=strides, 
                             padding='same', activation = tf.nn.relu)
    max_pool_1 = tf.layers.max_pooling1d(inputs=conv1, pool_size=2, strides=2, padding='same')
    
    # (batch, 64, 18) --> (batch, 32, 36)
    conv2 = tf.layers.conv1d(inputs=max_pool_1, filters=filters*2, kernel_size=kernel_size, strides=strides, 
                             padding='same', activation = tf.nn.relu)
    max_pool_2 = tf.layers.max_pooling1d(inputs=conv2, pool_size=2, strides=2, padding='same')
    
    # (batch, 32, 36) --> (batch, 16, 72)
    conv3 = tf.layers.conv1d(inputs=max_pool_2, filters=filters*2*2, kernel_size=kernel_size, strides=strides, 
                             padding='same', activation = tf.nn.relu)
    max_pool_3 = tf.layers.max_pooling1d(inputs=conv3, pool_size=2, strides=2, padding='same')
    
    # (batch, 16, 72) --> (batch, 8, 144)
    conv4 = tf.layers.conv1d(inputs=max_pool_3, filters=filters*2*2*2, kernel_size=kernel_size, strides=strides, 
                             padding='same', activation = tf.nn.relu)
    max_pool_4 = tf.layers.max_pooling1d(inputs=conv4, pool_size=2, strides=2, padding='same')
    
    with tf.Session() as sess:
        # 初始化
        tf.global_variables_initializer().run()
        # 输出卷积值
        conv = sess.run(max_pool_4, feed_dict = {input_b:b})
        #print(conv)
        print('len(conv):', np.size(conv))

conv4_pool(filters=4, kernel_size=3, strides=2)

print('---------- example 6 max pool ----------------')
def conv4(filters=2, kernel_size=3, strides=2):
    # (batch, 128, 9) --> (batch, 64, 18)
    conv1 = tf.layers.conv1d(inputs=input_b, filters = filters, kernel_size = kernel_size, strides = strides, 
                             padding='same', activation = tf.nn.relu)
    
    # (batch, 64, 18) --> (batch, 32, 36)
    conv2 = tf.layers.conv1d(inputs=conv1, filters=4, kernel_size = kernel_size, strides = strides, 
                             padding='same', activation = tf.nn.relu)
    
    # (batch, 32, 36) --> (batch, 16, 72)
    conv3 = tf.layers.conv1d(inputs=conv2, filters=8, kernel_size = kernel_size, strides = strides, 
                             padding='same', activation = tf.nn.relu)
    
    # (batch, 16, 72) --> (batch, 8, 144)
    conv4 = tf.layers.conv1d(inputs=conv3, filters=16, kernel_size = kernel_size, strides = strides, 
                             padding='same', activation = tf.nn.relu)
    
    print conv4
    with tf.Session() as sess:
        # 初始化
        tf.global_variables_initializer().run()
        conv = sess.run(conv3, feed_dict = {input_b:b})
        #print(conv)
        print('len(conv3):', np.size(conv))
        # 输出卷积值
        conv = sess.run(conv4, feed_dict = {input_b:b})
        #print(conv)
        print('len(conv4):', np.size(conv))

conv4(filters=2, kernel_size=3, strides=2)
print('---------- example 6 max pool ----------------')
conv4(filters=2, kernel_size=3, strides=4)

print('---------- example 7 max pool ----------------')
def conv4(filters=2, kernel_size=3, strides=2):
    # (batch, 128, 9) --> (batch, 64, 18)
    conv1 = tf.layers.conv1d(inputs=input_b, filters=2, kernel_size=3, strides=2, 
                             padding='same', activation = tf.nn.relu)
    max_pool_1 = tf.layers.max_pooling1d(inputs=conv1, pool_size=2, strides=2, padding='same')
    
    # (batch, 64, 18) --> (batch, 32, 36)
    conv2 = tf.layers.conv1d(inputs=conv1, filters=4, kernel_size=3, strides=2, 
                             padding='same', activation = tf.nn.relu)
    
    # (batch, 32, 36) --> (batch, 16, 72)
    conv3 = tf.layers.conv1d(inputs=conv2, filters=8, kernel_size=3, strides=2, 
                             padding='same', activation = tf.nn.relu)
    
    # (batch, 16, 72) --> (batch, 8, 144)
    conv4 = tf.layers.conv1d(inputs=conv3, filters=16, kernel_size=3, strides=2, 
                             padding='same', activation = tf.nn.relu)
    
    print conv4
    with tf.Session() as sess:
        # 初始化
        tf.global_variables_initializer().run()
        # 输出卷积值
        conv = sess.run(conv3, feed_dict = {input_b:b})
        #print(conv)
        print('len(conv3):', np.size(conv))
        conv = sess.run(conv4, feed_dict = {input_b:b})
        #print(conv)
        print('len(conv4):', np.size(conv))

conv4(filters=2, kernel_size=3, strides=2)
