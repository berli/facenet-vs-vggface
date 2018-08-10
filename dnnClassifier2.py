#!/usr/bin/python
# -*- coding: utf8 -*-)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
from six.moves.urllib.request import urlopen
import numpy as np
import tensorflow as tf


# 数据集
IRIS_TRAINING = "iris_training.csv"
IRIS_TRAINING_URL = "http://download.tensorflow.org/data/iris_training.csv"
IRIS_TEST = "iris_test.csv"
IRIS_TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset

def main():
    # 先将数据集保存到本地
    if not os.path.exists(IRIS_TRAINING):
        raw = urlopen(IRIS_TRAINING_URL).read()
        with open(IRIS_TRAINING, "wb") as f:
            f.write(raw)

    if not os.path.exists(IRIS_TEST):
        raw = urlopen(IRIS_TEST_URL).read()
        with open(IRIS_TEST, "wb") as f:
            f.write(raw)
            
    # 读取数据集
    training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=IRIS_TRAINING,
            target_dtype=np.int,
            features_dtype=np.float32)
    test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=IRIS_TEST,
            target_dtype=np.int,
            features_dtype=np.float32)

    #特征列x, 有四个维度
    feature_columns = [tf.feature_column.numeric_column("x", shape=[4])]

    # 创建一个三层的DNN深度学习分类器，三层分别有10、20、10个神经元
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
            hidden_units=[10, 20, 10], #三层分别有10、20、10个神经元
            n_classes=3, #三个分类
            model_dir="iris_model")

    print("training_set.target:",len(training_set.target),training_set.target)
    # 定义训练用的数据集输入
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": np.array(training_set.data)},
            y=np.array(training_set.target),
            num_epochs=None,
            shuffle=True)

    # 训练模型
    classifier.train(input_fn=train_input_fn, steps=2000)
    
    # 定义测试用的数据集输入
    test_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": np.array(test_set.data)},
            y=np.array(test_set.target),
            num_epochs=1,
            shuffle=False)

    # 评估准确率
    accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
    print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

    # 预测两个新样本
    new_samples = np.array(
    [[6.4, 3.2, 4.5, 1.5],
    [5.8, 3.1, 5.0, 1.7]], 
    dtype=np.float32)

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": new_samples},
    num_epochs=1,
    shuffle=False)

    predictions = list(classifier.predict(input_fn=predict_input_fn))
    print(
    "New Samples, Class Predictions:    {}\n"
    .format(predictions))
    predicted_classes = [p["classes"] for p in predictions]
    print(
    "New Samples, Class Predictions:    {}\n"
    .format(predicted_classes))

    # Generate predictions from the model
    ''''
    expected = ['Setosa', 'Versicolor', 'Virginica']
    predict_x = {
        'SepalLength': [5.1, 5.9, 6.9],
        'SepalWidth': [3.3, 3.0, 3.1],
        'PetalLength': [1.7, 4.2, 5.4],
        'PetalWidth': [0.5, 1.5, 2.1],
    }
    
    predictions = classifier.predict(
        input_fn=lambda:eval_input_fn(predict_x,
            labels=None,
            batch_size=100))
    #predict 方法返回一个 Python 可迭代对象，为每个样本生成一个预测结果字典。以下代码输出了一些预测及其概率：
    
    template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')
    
    for pred_dict, expec in zip(predictions, expected):
        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]
    
        print(template.format(iris_data.SPECIES[class_id],
                          100 * probability, expec))

    '''
if __name__ == "__main__":
    main()


