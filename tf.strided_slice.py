import tensorflow as tf
data = [1,2,3,4,5,6,7,8]
x = tf.strided_slice(data,[0],[5],[2])
y = tf.strided_slice(data,[1],[5])
print('data:',data)
print(x.numpy())
print(y.numpy())

data = [[1,2,3,4,5,6,7,8],[11,12,13,14,15,16,17,18]]
x = tf.strided_slice(data,[0,0],[1,4])
y = tf.strided_slice(data,[1,1],[2,5])
print('data:',data)
print(x.numpy())
print(y.numpy())
