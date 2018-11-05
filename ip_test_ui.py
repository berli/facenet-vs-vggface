
# -*- coding: utf-8 -*-)
import urllib2
import time
from Tkinter import *           # 导入 Tkinter 库

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    print(size)
    root.geometry(size)


def get_ip():

    response = urllib2.urlopen("http://2018.ip138.com/ic.asp")
    res = response.read()
    pos = res.find('[')
    pos1 = res.find(']')
    
    ip = res[pos+1:pos1]
    print ip

root = Tk()                     # 创建窗口对象的背景色
listb  = Listbox(root)          #  创建两个列表组件
root.maxsize(600, 400)
center_window(root, 600, 400)

if __name__ == '__main__':

    last_ip = "";
    while True:
        ip = get_ip();
        if( ip == ""):
            sleep(2)
            print '没有网络...'
            continue
        
        tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( time.time() ) )
        msg = tstr + ' 当前IP：'
        msg = msg+str(ip)
        listb.insert(0,msg)
        listb.pack()                    # 将小部件放置到主窗口中
        if( last_ip != "" and ip != last_ip):
            fp = popen("netsh interface set interface eth0 disabled")
            fp.read();
            fp1 = popen("netsh interface set interface wlan0 disabled")
            fp1.read();
            
            last_ip = ip;

        time.sleep(1)
        root.mainloop()                 # 进入消息循环
