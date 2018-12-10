import tensorflow as tf
w1 = tf.Variable([[1,2]], dtype=tf.float32)  
res = tf.matmul(w1, tf.cast([[2],[1]], dtype=tf.float32))  
grads = tf.gradients(res,w1)  
with tf.Session() as sess:  
    tf.global_variables_initializer().run()
    print(sess.run(res))
    print(sess.run(grads))
