import tensorflow as tf

x = tf.Variable(2.0)
y = x**2 + x - 1

grad = tf.gradients(y, x)

#######
w1 = tf.Variable([[1,2]], dtype = tf.float32)
#w1 = tf.Variable(tf.random_normal(shape=[1,2], dtype = tf.float32))
w2 = tf.Variable([[2],[1]], dtype=tf.float32)

res = tf.matmul(w1, w2)
#res1 = tf.matmul(w1, [[2],[1]])

#grads = tf.gradients(res,[w1,w2])
grads = tf.gradients(w1,w1)
#grads1 = tf.gradients(ys = res1, xs = [w1])


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    re = sess.run(grad)
    print('y:',re)
    re = sess.run(grads)
    print('res:',re)
    #re = sess.run(grads1)
    #print('res1:',re)

