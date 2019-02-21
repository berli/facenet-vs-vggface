
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
    return ip

if __name__ == '__main__':

    last_ip = "";
    f = open('log', 'a+')

    while True:
        ip = get_ip();
        if( ip == ""):
            sleep(2)
            print '没有网络...'
            continue
        print type(ip)
        tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( time.time() ) )
        msg = tstr + ' 当前IP：'
        msg = msg+str(ip)

        f.write(msg+'\n')

        if( last_ip != "" and ip != last_ip):
            msg = 'IP发生变化，禁用网卡'
            fp = popen("netsh interface set interface eth0 disabled")
            fp.read();
            fp1 = popen("netsh interface set interface wlan0 disabled")
            fp1.read();
            
            last_ip = ip;
            f.write(msg+'\n')

        time.sleep(1)
