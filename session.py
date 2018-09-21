#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf
import time as t
import collections

x = tf.Variable([1.0])
c = 1.0
a = tf.constant([10,20])
b = tf.constant([1.0, 2.0])
'''
The `fetches` argument may be a single graph element, or an arbitrarily
nested list, tuple, namedtuple, dict, or OrderedDict containing graph
elements at its leaves.  A graph element can be one of the following types:
* An @{tf.Operation}.
  The corresponding fetched value will be `None`.
* A @{tf.Tensor}.
  The corresponding fetched value will be a numpy ndarray containing the
  value of that tensor.
* A @{tf.SparseTensor}.
  The corresponding fetched value will be a
  @{tf.SparseTensorValue}
  containing the value of that sparse tensor.
* A `get_tensor_handle` op.  The corresponding fetched value will be a
  numpy ndarray containing the handle of that tensor.
* A `string` which is the name of a tensor or operation in the graph.
The value returned by `run()` has the same shape as the `fetches` argument,
where the leaves are replaced by the corresponding values returned by
TensorFlow.
Example:
python
   a = tf.constant([10, 20])
   b = tf.constant([1.0, 2.0])
   # 'fetches' can be a singleton
   v = session.run(a)
   # v is the numpy array [10, 20]
   # 'fetches' can be a list.
   v = session.run([a, b])
   # v is a Python list with 2 numpy arrays: the 1-D array [10, 20] and the
   # 1-D array [1.0, 2.0]
   # 'fetches' can be arbitrary lists, tuples, namedtuple, dicts:
   MyData = collections.namedtuple('MyData', ['a', 'b'])
   v = session.run({'k1': MyData(a, b), 'k2': [b, a]})
   # v is a dict with
   # v['k1'] is a MyData namedtuple with 'a' (the numpy array [10, 20]) and
   # 'b' (the numpy array [1.0, 2.0])
   # v['k2'] is a list with the numpy array [1.0, 2.0] and the numpy array
   # [10, 20].
'''
with tf.Session() as sess:
    v = sess.run(a)
    print 'session a =', v
    
    v = sess.run([a,b])
    print 'session [a, b] =',v
    
    v = sess.run([a,b*2])
    print 'session [a, b*2] =',v

    MyData = collections.namedtuple('MyData', ['a', 'b'])
    v = sess.run({'k1':MyData(a, b), 'k2':[b, a] } )
    print 'Mydata =',v

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    s1 = t.time()
    #通过step run的方式读取变量
    for i in range(100000):
        res = sess.run(x)
    print "通过sess.run读取变量的时间:",t.time() - s1

    s2 = t.time()
    for i in range(100000):
        a = b
    print "通过直接赋值的时间:", t.time() - s2


