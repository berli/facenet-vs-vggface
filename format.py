#!/usr/bin/python
# -*- coding:utf8 -*- 

import time

def formatData(file1, file2):
    f = open(file1, 'r')
    fw = open(file2, 'w')
    for line in f:
        #print line;
        i = 0;
        new = "";
        num = len(line.strip('\r\n').split(","))
        #print num
        for elem in line.strip('\r\n').split(","):
            if( elem.find('\N') != -1):
                new += "0";
            else:
                new += elem

            if( i != num-1 ):
                new += ','
            i+=1;

        #print "new:"+new
        fw.write(new+'\r\n');


if __name__=='__main__':  
    
    formatData('clean.csv', 'format.csv')
