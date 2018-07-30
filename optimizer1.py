#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

print '求goal最小值...'
#目标函数 goal = (x-3)的平方,求goal最小时，x的值
x = tf.Variable(tf.truncated_normal([1], name='x'));
goal = tf.pow(x-3, 2, name='goal')

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #x.initializer.run()
    print 'x:',x.eval()
    print 'goal:',goal.eval()

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train_step = optimizer.minimize(goal)

def train():
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer());
        for i in range(10):
            print 'x:',x.eval();
            train_step.run();
            print 'goal:',goal.eval()

train()

#求goal最大值
print '\n\n求goal最大值...'
y = tf.Variable(tf.truncated_normal([1], name='x'))
max_goal = tf.sin(y)
#max_goal = y
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
train_step = optimizer.minimize(tf.negative(max_goal))
#train_step = optimizer.minimize(-1*max_goal)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(10):
        print 'y:', y.eval()
        train_step.run()
        print 'max_goal:',max_goal.eval()

#minimize() = compute_gradients() + apply_gradients()
#从上面的minimize函数开始,其他不变
print '\n\nminimize() = compute_gradients() + apply_gradients()\n\n'

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
#gra_and_var = optimizer.compute_gradients(tf.negative(max_goal))
gra_and_var = optimizer.compute_gradients(goal)
train_step = optimizer.apply_gradients(gra_and_var);
#train_step = optimizer.minimize(-1*max_goal)
train()

print '\n\nclip_by_global_norm:修正梯度值'
gradients, variables = zip(*optimizer.compute_gradients(goal))
gradients, _= tf.clip_by_global_norm(gradients, 1.25)
train_step = optimizer.apply_gradients(zip(gradients, variables))
train()

#exponential_decay 加入学习率衰减
print '\n\nexponential_decay 加入学习率衰减\n\n'
#global_step 记录当前是第几个batch
global_step = tf.Variable(0)
learning_rate = tf.train.exponential_decay(
        3.0, global_step, 3, 0.3, staircase=True)
optimizer2 = tf.train.GradientDescentOptimizer(learning_rate)
gradients, variables = zip(*optimizer2.compute_gradients(goal))
gradients, _ = tf.clip_by_global_norm(gradients, 1.25)
train_step = optimizer2.apply_gradients(zip(gradients, variables), global_step=global_step)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    global_step.initializer.run()
    for i in range(10):
        print "x: ",x.eval()
        train_step.run()
        print "goal: ", goal.eval()
