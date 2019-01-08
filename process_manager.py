'''************************************************************************
    > File Name: process_manager.py
    > Author: libo
    > Mail: libo2@huya.com 
    > Created Time: Mon 03 Dec 2018 11:42:33 AM CST
 *********************************************************************'''
#!/usr/bin/python

import psutil
import signal
import time
import os
import sys

def specific_pid(p_name_list):
    pids = psutil.pids()

    pname_list = {}
    for p in p_name_list:
        pname_list[p] = False;
    for pid in pids:
        p = psutil.Process(pid)
        args = p.cmdline()
        #print 'args:',args
        cluster_flags = 0
        for arg in args:
            for p in p_name_list:
                if(arg.find(p) != -1 ):
                    pname_list[p] = True;
                    break;

    return pid_list;

last_pid_list = {}
last_pid_dic ={}
found = False
while True:
    cur_time = time.time()
    pid_list = specific_pid()
    for pid in pid_list:
        last_pid_dic[pid]=cur_time

    last_pid_list = pid_list;
    if( True):
    #if( len(last_pid_dic) < 5):
        #if( found ):
        if( True ):
            for pid,v in last_pid_list.items():
                os.kill(pid, signal.SIGKILL)
                print 'kill ',pid
                found = False
        else:
            found = True
    else:
        print('cluster work fine:',last_pid_list)

    time.sleep(600)

if __name__ == '__main__':
