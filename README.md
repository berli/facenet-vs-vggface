# facenet-vs-vggface
file1    file2    facenet(欧式距离)  vggface(余弦相似度)
gg1.jpg  gg2.jpg  0.6976             0.74451
gg1.jpg  gg3.jpg  0.7641             0.626138
gg1.jpg  gg5.jpg  0.7882             0.58714
gg1.jpg  gg6.jpg  no detect          0.473986
gg1.jpg  gg7.jpg  no detect          0.475262
6.jpg    33.jpg   0.6209             0.467728
gg2.jpg  gg3.jpg  0.7289             0.646415
g2.jpg   gg5.jpg  0.8284             0.684934
gg2.jpg  gg6.jpg  no detect          0.560137
gg3.jpg  gg5.jpg  0.6176             0.619669
rr.jpg   rr2.jpg  0.5816             0.545326

PS:facenet是基于tensorflow实现,vggface是基于caffe实现
还有TensorFlow的facenet运行相当慢，耗时是caffe的5倍
