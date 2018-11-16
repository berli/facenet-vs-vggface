import tensorflow as tf

a = tf.Variable(1)
b = tf.Variable(2)
c = tf.add(a, b)

saver = tf.train.Saver()
saver_hook = tf.train.CheckpointSaverHook('./testpot/', 
                                          save_steps=2, 
                                          saver=saver)

global_step = tf.Variable(0, name='global_step', trainable=False)
summary_op = tf.summary.scalar('c', c)
summary_hook = tf.train.SummarySaverHook(save_steps=2, 
                                         summary_op=summary_op)
with tf.train.MonitoredTrainingSession(hooks=[saver_hook, summary_hook]) as sess:
    while not sess.should_stop():
        print(sess.run(c))
