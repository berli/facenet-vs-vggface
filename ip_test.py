
# -*- coding: utf-8 -*-)
import urllib2
import time

def get_ip():

    response = urllib2.urlopen("http://2018.ip138.com/ic.asp")
    res = response.read()
    pos = res.find('[')
    pos1 = res.find(']')
    
    ip = res[pos+1:pos1]
    print ip

if __name__ == '__main__':

    last_ip = "";
    while True:
        ip = get_ip();
        if( ip == ""):
            sleep(2)
            print '没有网络...'
            continue

        if( last_ip != "" and ip != last_ip):
            fp = popen("netsh interface set interface eth0 disabled")
            fp.read();
            fp1 = popen("netsh interface set interface wlan0 disabled")
            fp1.read();
        time.sleep(1)
