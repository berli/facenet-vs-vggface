#!/usr/bin/python
# -*- coding:utf8 -*-

import tensorflow as tf
import numpy as np 

list_of_points1_ = [[1,2], [3,4], [5,6], [7,8]]
list_of_points2_ = [[15,16], [13,14], [11,12], [9,10]]
 
list_of_points1 = np.array([np.array(elem).reshape(1,2) for elem in list_of_points1_])
list_of_points2 = np.array([np.array(elem).reshape(1,2) for elem in list_of_points2_])
 
 
graph = tf.Graph()
 
with graph.as_default():   
 
    #我们使用 tf.placeholder() 创建占位符 ，在 session.run() 过程中再投递数据 
    point1 = tf.placeholder(tf.float32, shape=(1, 2))
    point2 = tf.placeholder(tf.float32, shape=(1, 2))
 
    def calculate_eucledian_distance(point1, point2):
        difference = tf.subtract(point1, point2)
        power2 = tf.pow(difference, tf.constant(2.0, shape=(1,2)))
        add = tf.reduce_sum(power2)
        eucledian_distance = tf.sqrt(add)
        return eucledian_distance
 
    dist = calculate_eucledian_distance(point1, point2)
 
 
with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()   
    for ii in range(len(list_of_points1)):
        point1_ = list_of_points1[ii]
        point2_ = list_of_points2[ii]
 
        #使用feed_dict将数据投入到[dist]中
        feed_dict = {point1 : point1_, point2 : point2_}
        distance = session.run([dist], feed_dict=feed_dict)
        print("the distance between {} and {} -> {}".format(point1_, point2_, distance))

