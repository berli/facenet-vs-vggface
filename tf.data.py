#!/usr/bin/python
# -*- coding: utf-8 -*-)

import tensorflow as tf

batch_size = 2

def decode_line(line):
    # Decode the line to tensor
    record_defaults = [[1.0] for col in range(8)]
    items = tf.decode_csv(line, record_defaults)
    features = items[0:6]
    label = items[7]

    label = tf.cast(label, tf.float32)
    #label = tf.one_hot(label, 20)

    return features,label

def create_dataset(filename, batch_size=2, is_shuffle=False, n_repeats=0):
    """create dataset for train and validation dataset"""
    dataset = tf.data.TextLineDataset(filename).skip(0)
    if n_repeats > 0:
        dataset = dataset.repeat(n_repeats)         # for train
    # dataset = dataset.map(decode_line).map(normalize)  
    dataset = dataset.map(decode_line)    
    # decode and normalize
    if is_shuffle:
        dataset = dataset.shuffle(10000)            # shuffle
    dataset = dataset.batch(batch_size)
    return dataset

training_filenames = ["queue_test.csv"] 
# replace the filenames with your own path

# Create different datasets
training_dataset = create_dataset(training_filenames, batch_size=2 )

# A reinitializable iterator is defined by its structure. We could use the
# `output_types` and `output_shapes` properties of either `training_dataset`
# or `validation_dataset` here, because they are compatible.
#iterator = tf.data.Iterator.from_structure(training_dataset.output_types,
#                                           training_dataset.output_shapes)
iterator = training_dataset.make_initializable_iterator()
features, labels = iterator.get_next()


# Using reinitializable iterator to alternate between training and validation.
with tf.Session() as sess:
    sess.run(iterator.initializer)
    i = 0
    while True:
        try:
            print("TRAIN\n",sess.run(labels))
            a = sess.run(labels)
            for i in a:
                print i
        except tf.errors.OutOfRangeError:
            break
        i += 1

