# facenet-vs-vggface
|file1    |   file2 | facenet(欧式距离) |  facenet(欧式距离-显卡)  | vggface(余弦相似度)  |     
| ------  | ------- | ---------------  | --------------------   | --------------- |  
|gg1.jpg  |gg2.jpg  |0.6976           |0.6545 |0.74451 |      
|gg1.jpg  |gg3.jpg  |0.7641           |<font color=#DC143C> 0.6883 </font> |0.626138|    
|gg1.jpg  |gg5.jpg  |0.7882           |0.7961  |0.58714 |    
|gg1.jpg  |gg6.jpg  |no detect        |   x     |0.473986|     
|gg1.jpg  |gg7.jpg  |no detect        |   x     |0.475262|     
|6.jpg    |33.jpg   |0.6209           |  x|0.467728|     
|gg2.jpg  |gg3.jpg  |0.7289           |0.7287  |0.646415|     
|g2.jpg   |gg5.jpg  |0.8284           |0.8286  |0.684934|     
|gg2.jpg  |gg6.jpg  |no detect        | x |0.560137|      
|gg3.jpg  |gg5.jpg  |0.6176           | 0.6175 |0.619669|      
|rr.jpg   |rr2.jpg  |0.5816           |  x|0.545326|   

PS:facenet是基于tensorflow实现,vggface是基于caffe实现   
还有TensorFlow的facenet运行相当慢，耗时是caffe的5倍


----------------------------------AI 学习路线图----------------------   
1 先熟悉TensorFlow，caffe的环境，能安装，跑demo  
2 从你感兴趣的课题切入，我比较感兴趣人脸识别，图像检测，觉得比较好玩，有兴趣才有动力嘛   
然后学习下文本处理，比如分词，文本摘要生成，从github或开源的代码寻找相关感兴趣的，然后试着改成你想要的  
4 自己尝试写一些力所能及的代码，体会其中的原理  
5 逐步深入，优化开源的，加大难度  

本来想以C++主要学习路线，caffe还可以全部用C++，TensorFlow就不行了，很多API只有python的
