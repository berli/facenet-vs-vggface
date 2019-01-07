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

def specific_pid():
    pids = psutil.pids()

    pid_list = {}
    for pid in pids:
        p = psutil.Process(pid)
        args = p.cmdline()
        #print 'args:',args
        cluster_flags = 0
        for arg in args:
            if(arg.find('multi_layer_cluster.py') != -1 ):
                cluster_flags = cluster_flags + 1
            if( arg.find('--job_name=worker') != -1):
                cluster_flags = cluster_flags + 1
            if( cluster_flags == 2):
                pid_list[pid] = p.name()
                print("pid-%d,pname-%s, arg:%s" %(pid,p.name(), p.cmdline() ))
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
