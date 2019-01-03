#!/usr/bin/python
# -*- coding: utf-8 -*-)
import os
import sys

def get_file(path):
    files= os.listdir(path)
    for file in files:
        if not os.path.isdir(file): #判断是否是文件夹
            print file

if __name__ == '__main__':
    get_file(sys.argv[1])
