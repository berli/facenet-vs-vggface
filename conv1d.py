# -*- coding: utf-8 -*-)
import tensorflow as tf
import numpy as np

# 定义一个矩阵a，表示需要被卷积的矩阵。
a = np.array(np.arange(1, 1 + 20).reshape([1, 10, 2]), dtype=np.float32)
print('a',a)
print('---------------------------')
# 卷积核，此处卷积核的数目为1
kernel = np.array(np.arange(1, 1 + 4), dtype=np.float32).reshape([2, 2, 1])
print('kernel',kernel)

# 进行conv1d卷积
conv1d = tf.nn.conv1d(a, kernel, 1, 'VALID')

with tf.Session() as sess:
    # 初始化
    tf.global_variables_initializer().run()
    # 输出卷积值
    print(sess.run(conv1d))

