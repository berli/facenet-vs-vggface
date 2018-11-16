from __future__ import print_function
import tensorflow as tf

def example():
    g1 = tf.Graph()
    with g1.as_default():
        # Define operations and tensors in `g`.
        c1 = tf.constant(42)
        assert c1.graph is g1

    g2 = tf.Graph()
    with g2.as_default():
        # Define operations and tensors in `g`.
        c2 = tf.constant(3.14)
        assert c2.graph is g2

    # MonitoredTrainingSession example
    with g1.as_default():
        with tf.train.MonitoredTrainingSession() as sess:
            print(c1.eval(session=sess))
            # Next line raises
            # ValueError: Cannot use the given session to evaluate tensor:
            # the tensor's graph is different from the session's graph.
            try:
                print(c2.eval(session=sess))
            except ValueError as e:
                print(e)

    # Session example
    with tf.Session(graph=g2) as sess:
        print(c2.eval(session=sess))
        # Next line raises
        # ValueError: Cannot use the given session to evaluate tensor:
        # the tensor's graph is different from the session's graph.
        try:
            print(c1.eval(session=sess))
        except ValueError as e:
            print(e)

if __name__ == '__main__':
    example()
