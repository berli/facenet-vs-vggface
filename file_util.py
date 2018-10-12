#!/usr/bin/python
# -*- coding: utf-8 -*-)

import os
import sys
import shutil
import cv2
import time


def clean_min_file(path):
    for file in os.listdir(path):
        full = os.path.join(path, file)
        if os.path.isdir(full):
            batch_rename(full)
            #print 'dir:',full
        else:
            #print 'file:',full
            fsize = os.path.getsize(full)
            fsize = fsize/1024;

            img = cv2.imread(full)
            if( img is None):
                if( full.find(".gif") != -1):
                    print full, ' continue'
                continue
            sp = img.shape
            #print sp
            height = sp[0]
            witdh = sp[1]
            #print full,' size:',fsize
            if(fsize < 10 or (height <= 100 and witdh <= 100)):
                os.remove(full)
                print 'remove:',full, ' size:',fsize,' Kb', ' shape:',sp

def batch_rename(path):
    for file in os.listdir(path):
        full = os.path.join(path, file)
        if os.path.isdir(full):
            batch_rename(full)
            #print 'dir:',full
        else:
            #print 'file:',full
            pos = full.find("╚¤╣·╤▌╥х_╡┌")
            pos += len("╚¤╣·╤▌╥х_╡┌")
            index = full[pos:pos+2]
            #print 'pos:', pos, ' index:',index
            new = str(index) + "_The.Three.Kingdoms.srt"
            #shutil.copyfile(full, path+"/"+new)
            #shutil.copyfile(full, new)


if __name__ == '__main__':
    if( len(sys.argv) > 1 ):
        #batch_rename(sys.argv[1])
        while True:
            clean_min_file(sys.argv[1])
            time.sleep(3600)
