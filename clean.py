#!/usr/bin/python
# -*- coding:utf8 -*- 

import time

def toMinute( timeStamp ):
    timeArray = time.localtime( float(timeStamp) )
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:00", timeArray)
    timeArray = time.strptime(otherStyleTime,"%Y-%m-%d %H:%M:%S")
    m = int(time.mktime(timeArray)) #minute
    return m;

def cleanData(file1, file2):
    f = open(file1, 'r')
    fw = open(file2, 'w')
    for line in f:
        #print line;
        i = 0;
        new = "";
        num = len(line.strip('\r\n').split(","))
        #print num
        for elem in line.strip('\r\n').split(","):
            if( i==0 or i== 2 or i==24):
                i+=1;
                continue;

            if( i== 1):
                new += str(toMinute(elem));
            else:
                new += elem

            if( i != num-2 ):
                new += ','
            i+=1;

        #print "new:"+new
        fw.write(new+'\r\n');


if __name__=='__main__':  
    
    cleanData('night10w.csv', 'clean.csv')
