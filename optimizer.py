#!/usr/bin/python

import tensorflow as tf

x = tf.Variable(2, name='x', dtype=tf.float32)
log_x = tf.log(x)
log_x_squared = tf.square(log_x)

optimizer = tf.train.GradientDescentOptimizer(0.25)
train = optimizer.minimize(log_x_squared)

init = tf.global_variables_initializer()

def optimize():
  with tf.Session() as session:
    session.run(init)
    print("starting at", "x:", session.run(x), "log(x):", session.run(log_x), "log(x)^2:", session.run(log_x_squared))
    for step in range(50):  
      session.run(train)
      print("train step", step, "x:", session.run(x), "log(x):", session.run(log_x), "log(x)^2:", session.run(log_x_squared))
        

optimize()
