import tensorflow as tf  
 
# calculate cross_entropy 
y  = tf.constant([[1.0, 2.0, 3.0, 4.0],[1.0, 2.0, 3.0, 4.0],[1.0, 2.0, 3.0, 4.0]])  
y_ = tf.constant([[0.0, 0.0, 0.0, 1.0],[0.0, 0.0, 0.0, 1.0],[0.0, 0.0, 0.0, 1.0]])  
ysoft = tf.nn.softmax(y)  
cross_entropy = -tf.reduce_sum(y_*tf.log(ysoft))  
 
#do cross_entropy just one step  
cross_entropy2=tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits_v2(logits = y, labels = y_))
 
cross_entropy_loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits = y, labels = y_))
 
with tf.Session() as sess:   
    print("step1:softmax result=")  
    print(sess.run(ysoft))  
    print("step2:cross_entropy result=")  
    print(sess.run(cross_entropy))  
    print("Function(softmax_cross_entropy_with_logits) result=")  
    print(sess.run(cross_entropy2))
    print("cross_entropy_loss result=")  
    print(sess.run(cross_entropy_loss))

