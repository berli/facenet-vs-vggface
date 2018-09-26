#!/usr/bin/python
# -*- coding: utf-8 -*-)
from sklearn import preprocessing

le = preprocessing.LabelEncoder()
le.fit(["paris", "paris", "tokyo", "amsterdam"]);
print "paris", "paris", "tokyo", "amsterdam"
print le.transform(["tokyo", "tokyo", "paris", "amsterdam", "amsterdam"]) 
