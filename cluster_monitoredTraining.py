'''*************************************************************************
    > File Name: cluster_gpu.py
    > Author: libo
    > Mail: libo2@huya.com 
    > Created Time: Wed 05 Nov 2018 05:53:17 PM CST
 *********************************************************************'''
#coding=utf-8
import numpy as np
import tensorflow as tf

#python cluster_monitoredTraining.py --ps_hosts=127.0.0.1:2222 --worker_hosts=127.0.0.1:2224,127.0.0.1:2225 --job_name=ps --task_index=0
#python cluster_monitoredTraining.py --ps_hosts=127.0.0.1:2222 --worker_hosts=127.0.0.1:2224,127.0.0.1:2225 --job_name=worker --task_index=0 
#python cluster_monitoredTraining.py --ps_hosts=127.0.0.1:2222 --worker_hosts=127.0.0.1:2224,127.0.0.1:2225 --job_name=worker --task_index=1 

# Define parameters
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_float('learning_rate', 0.00003, 'Initial learning rate.')
tf.app.flags.DEFINE_integer('steps_to_validate', 1000,
                     'Steps to validate and print loss')

# For distributed
tf.app.flags.DEFINE_string("ps_hosts", "",
                           "Comma-separated list of hostname:port pairs")
tf.app.flags.DEFINE_string("worker_hosts", "",
                           "Comma-separated list of hostname:port pairs")
tf.app.flags.DEFINE_string("job_name", "", "One of 'ps', 'worker'")
tf.app.flags.DEFINE_string("log_dir", "log", "log dir")
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task within the job")
tf.app.flags.DEFINE_integer("gpu_num", 1, "number of GPU for the job")
tf.app.flags.DEFINE_integer("train_max_step", 1000000, "number of training max step")

# Hyperparameters
learning_rate = FLAGS.learning_rate
steps_to_validate = FLAGS.steps_to_validate

def main(_):
  
  ps_hosts = FLAGS.ps_hosts.split(",")
  worker_hosts = FLAGS.worker_hosts.split(",")
  cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})
  server = tf.train.Server(cluster,job_name=FLAGS.job_name,task_index=FLAGS.task_index)

  if FLAGS.job_name == "ps":
    server.join()
  elif FLAGS.job_name == "worker":
      with tf.device(tf.train.replica_device_setter(
          worker_device="/job:worker/task:%d" %(FLAGS.task_index), 
          cluster=cluster)):
          global_step = tf.Variable(0, name='global_step', trainable=False)

          #input = tf.placeholder(shape=[1,1], dtype=tf.float32)
          #label = tf.placeholder(shape=[1], dtype=tf.float32)
          input = tf.placeholder_with_default(input =[[0.122515]], shape=[1,1])
          label = tf.placeholder_with_default(input = [1.0], shape=[1])

          weight = tf.get_variable(name = "weight", shape=[1,1], dtype = tf.float32, initializer=tf.random_normal_initializer())
          biase  = tf.get_variable(name = "biase", shape = [1,1], dtype = tf.float32, initializer=tf.random_normal_initializer())
          pred = tf.matmul(input, weight) + biase

          loss_value = loss(label, pred)

          train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_value, global_step=global_step)
          init_op = tf.global_variables_initializer()

          saver = tf.train.Saver()
          #tf.summary.scalar('cost', loss_value)
          tf.summary.tensor_summary('cost', loss_value)
          summary_op = tf.summary.merge_all()

      #sv = tf.train.Supervisor(is_chief=(FLAGS.task_index == 0),
      #                        logdir="./checkpoint/",
      #                        init_op=init_op,
      #                        summary_op=None,
      #                        saver=saver,
      #                        global_step=global_step,
      #                        save_model_secs=60)      
      #with sv.managed_session(server.target) as sess:
      summary_hook = tf.train.SummarySaverHook(save_secs=600,output_dir=FLAGS.log_dir,summary_op=summary_op)
      #sess_config = tf.ConfigProto(gpu_options = tf.GPUOptions(allow_growth=True), allow_soft_placement = True, log_device_placement = False)
      sess_config = tf.ConfigProto( allow_soft_placement = True, log_device_placement = False)
      hooks = [tf.train.StopAtStepHook(last_step = FLAGS.train_max_step), summary_hook]

      with tf.train.MonitoredTrainingSession(master=server.target,
                              is_chief=(FLAGS.task_index == 0),
                              checkpoint_dir="./checkpoint/",
                              config=sess_config,
                              save_checkpoint_secs=60) as sess:
          step = 0
          while  not sess.should_stop():
            train_x = np.random.random((1,1))
            #print 'train_x:',train_x
            train_y =  np.random.randn(1) * 0.33  + 10
            _, loss_v, step = sess.run([train_op, loss_value,global_step], feed_dict={input:train_x, label:train_y})
            if step % steps_to_validate == 0:
              w,b = sess.run([weight,biase])
              print("step: %d, weight: %f, biase: %f, loss: %f" %(step, w, b, loss_v))


def loss(label, pred):
  return tf.square(label - pred)



if __name__ == "__main__":
  tf.app.run()
