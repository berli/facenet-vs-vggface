# -*- coding: utf-8 -*-)
import tensorflow as tf  

#our NN's output  
logits=tf.constant([[1.0,2.0,3.0],[1.0,2.0,3.0],[1.0,2.0,3.0]])  
#step1:do softmax  
y=tf.nn.softmax(logits)  
#true label 
#注意这里标签必须是浮点数,不然在后面计算tf.multiply时就会因为类型不匹配tf_log的float32数据类型而出错
y_=tf.constant([[0,0,1.0],[0,0,1.0],[0,0,1.0]])#这个是稀疏的标签
#step2:do log  
tf_log=tf.log(y)
#step3:do mult  
pixel_wise_mult=tf.multiply(y_,tf_log)
#step4:do cross_entropy  
cross_entropy = -tf.reduce_sum(pixel_wise_mult)  
 
#do cross_entropy just two step  
#将标签稠密化
print('y_',y_)
dense_y=tf.argmax(y_,1)
print('dense_y:',dense_y)

cross_entropy2_step1=tf.nn.sparse_softmax_cross_entropy_with_logits(labels=dense_y,logits=logits)
cross_entropy2_step2=tf.reduce_sum(cross_entropy2_step1)#dont forget tf.reduce_sum()!!  

y_value,tf_log_value,pixel_wise_mult_value,cross_entropy_value=y,tf_log,pixel_wise_mult,cross_entropy
sparse_cross_entropy2_step1_value,sparse_cross_entropy2_step2_value=cross_entropy2_step1,cross_entropy2_step2
print("step1:softmax result=\n%s\n"%(y_value))
print("step2:tf_log_result result=\n%s\n"%(tf_log_value))
print("step3:pixel_mult=\n%s\n"%(pixel_wise_mult_value))
print("step4:cross_entropy result=\n%s\n"%(cross_entropy_value))
print("Function(softmax_cross_entropy_with_logits) result=\n%s\n"%(sparse_cross_entropy2_step1_value))  
print("Function(tf.reduce_sum) result=\n%s\n"%(sparse_cross_entropy2_step2_value))

