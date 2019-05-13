
#-*- coding: utf-8 -*-)
import tensorflow as tf
import tempfile

ds_tensors = tf.data.Dataset.from_tensor_slices([1,2,3,4,5,6])
_,filename = tempfile.mkstemp()

with open(filename, 'w') as f:
    f.write("""Line 1
    Line 2
    Line 3
    """)

    ds_file = tf.data.TextLineDataset(filename)

ds_tensors = ds_tensors.map(tf.square).shuffle(2).batch(2)
ds_file = ds_file.batch(2)

print("Elements of ds_tensors")
for x in ds_tensors:
    print(x)

for x in ds_file:
    print(x)
