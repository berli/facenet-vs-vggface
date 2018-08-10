#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf
import numpy as np

#特征列表
feature_columns = [tf.feature_column.numeric_column("x", shape=[1])]

#创建线性回归,线性分类,神经网络分类
estimator = tf.estimator.LinearRegressor(feature_columns = feature_columns)

#创建训练数据
x_train = np.array([1.,2.,3.,4.])
y_train = np.array([0.,-1.,-2.,-3.])
x_eval = np.array([2.,5.,8.,1.])
y_eval = np.array([-1.01,-4.1,-7.,0.])

input_fn = tf.estimator.inputs.numpy_input_fn({'x':x_train}, y_train, batch_size=4, num_epochs= None, shuffle=True)
train_input_fn = tf.estimator.inputs.numpy_input_fn({'x':x_train}, y_train, batch_size=4, num_epochs=1000, shuffle=False)
eval_input_fn = tf.estimator.inputs.numpy_input_fn({'x':x_train}, y_eval, batch_size=4, num_epochs=1000, shuffle=False)

#训练
estimator.train(input_fn = input_fn, steps=1000)

train_metrics= estimator.evaluate(input_fn = train_input_fn)
eval_metrics = estimator.evaluate(input_fn = eval_input_fn)
eval_pre = estimator.predict(input_fn = eval_input_fn)

print 'train metrics:%r'%train_metrics
print 'eval metrics:%r'%eval_metrics

for i in eval_pre:
    print 'predict:',i
