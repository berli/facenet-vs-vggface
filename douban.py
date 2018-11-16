
# -*- coding: utf-8 -*-)
import urllib2
import time
from bs4 import BeautifulSoup
import sys
import random
reload(sys) 
sys.setdefaultencoding('utf-8')

import socket
 
_dnscache={}
def _setDNSCache():
    """
    Makes a cached version of socket._getaddrinfo to avoid subsequent DNS requests.
    """
 
    def _getaddrinfo(*args, **kwargs):
        global _dnscache
        if args in _dnscache:
            print str(args)+" in cache"
            return _dnscache[args]
 
        else:
            print str(args)+" not in cache"  
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]
 
    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo
 

def get_article_link(url):
    try:
        response = urllib2.urlopen(url)
        res = response.read()
    except HTTPError as e:
        content = e.read()
        print('exception:',content)
        print('sleep 10s....')
        time.sleep(10)
    bsObj = BeautifulSoup(res, 'html.parser')
    links = bsObj.find_all('a')
    articles = {}
    kind = {}
    max = 0;
    for link in links:
        l = str(link.get('href'))
        #print 'links:',l
        #print 'urls:',urls
        #print 'type(l):',type(l)
        if( l.find('/ebook/') == 0):
            articles['https://read.douban.com/'+l]='1'
        if( l.find('/kind/0/') == 0 or l.find('/kind/500/') == 0):
            print '跳过全部:',l
            time.sleep(5);
            continue;
        active_title = ""
        if( l.find('/kind/') == 0):
            print 'l:',l
            for bs in bsObj.find_all('a', {'href':l}, class_='title active'):
                print 'active_kind_title:', bs.text
                active_title = bs.text
                kind['https://read.douban.com'+l] = bs.text
            for bs in bsObj.find_all('a', {'href':l}, class_='title'):
                print 'kind_title:', bs.text
                kind['https://read.douban.com'+l] = bs.text
        if( l.find('https://read.douban.com/column/') == 0):
            articles[l] = active_title
        elif( l.find('?start=') == 0):
            pos = l.find('?start=')
            pos1 = l.find('&', pos)
            if( pos1  != -1):
                start = l[pos+len('?start='):pos1]
                if( int(start) > max):
                    max = int(start)
                print start
                print l

    return articles, max, kind

def get_article(url):

    response = urllib2.urlopen(url)
    bsObj = BeautifulSoup(response, 'lxml')
    line = ''
    for read in  bsObj.find_all('h1', class_='article-title'):
        print 'title:', read.text
        line = read.text.encode("utf-8")
        line +=','
    #专栏
    special = False;
    if(len(line) == 0):
        for read in  bsObj.find_all('h1', class_='title-wrapper'):
            print 'specail title:', read.text
            line = read.text.replace('\n','').encode("utf-8")
            line +=','
            special = True;

    #评分
    flag = False
    for read in  bsObj.find_all('span', class_='score'):
        line += read.text
        line +=','
        print 'score:', read.text
        flag = True;
    if(len(line) > 0 and not flag):
        line +='0,'

    #评价人数
    for read in  bsObj.find_all('span', class_='amount'):
        print 'rate people:', read.text.split()[0]
        line += read.text.split()[0]
        line +=','
    if( len(line)> 0 and len(bsObj.find_all('span', class_='amount')) == 0):
        line +='0,'
   
   #定价
    price = 0 
    for read in  bsObj.find_all('span', class_='current-price-count'):
        print 'price:', read.text.replace('￥', '')
        if( read.text.find('免费') == -1):
            price = float(read.text.replace('￥', ''))
            print 'price:', price
            if( price > 0.0 ):
                line += read.text.replace('￥', '')
                line +=','
        else:
            #line += read.text.replace('￥', '')
            line +='0,'

    #折扣价
    discount = False;
    for read in  bsObj.find_all('span', class_='discount-price current-price-count'):
        print 'discount-price:', read.text.replace('￥', '')
        line += read.text.replace('￥', '')
        line +=','
        discount = True;
    #原价
    if(not discount ):
        for read in  bsObj.find_all('s', class_='original-price-count'):
            print 'original-price:', read.text.replace('￥', '')
            if( float(read.text.replace('￥', '')) > 0):
                price = float(read.text.replace('￥', ''))
                line += read.text.replace('￥', '')
                line +=','
    if(special):
        line +='0,'

    #阅读人数
    if( not special):
        for read in  bsObj.find_all('span', class_='read-count'):
            print 'read-count:', read.text.split()[0]
            line += read.text.split()[0];
    else:
        #专栏
        special_count = 0;
        for read in  bsObj.find_all('span', class_='count'):
            cnt = int(read.text.replace(',',''))
            if(cnt > special_count):
                special_count = cnt
        line += str(special_count)
        print 'specail read-count:', special_count


    return line

def get_kind(kind, kind_title):

    #url = "https://read.douban.com/kind/532?start=0&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    url = "https://read.douban.com/kind/{0}?start=0&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    get_url = "https://read.douban.com/kind/{0:d}?start={1:d}&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    
    links,max, _ = get_article_link(url.format(kind))
    page_url =[]
    
    if( max > 20):
        for i in range(20, max, 20):
            cur_url = get_url.format(int(kind), i)
            page_url.append(cur_url)
            #print 'page_url:',page_url

    now = time.time()
    day = time.strftime("%Y-%m-%d", time.localtime(now))
    title ='article_' +kind_title+'_' +day + '.txt'
    print 'file:',title

#sudo pip install BeautifulSoup4 lxml
    f = open(title, 'w')
    #爬取一个分类的文章
    for url in page_url:
        temp={}
        #爬取一篇文章的内容
        for article,v in links.items():
            print 'article:',article
            line = get_article(article)
            temp[line] = '1'
            print 'temp:',temp

            #防止被封IP
            stop = random.randint(1, 5)
            print 'sleep:',stop
            time.sleep(stop)

        for line,v in temp.items():
            if( len(line) > 0):
                f.write(line+'\n')
                f.flush()
        print 'get url:',url
        links,max, _ = get_article_link(url)


if __name__ == '__main__':

    url = "https://read.douban.com/kind/532?start=0&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    get_url = "https://read.douban.com/kind/532?start={0:d}&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    
    _setDNSCache()
    links,max, kind_url = get_article_link(url)
    page_url =[]
    
    if( max > 20):
        for i in range(20, max, 20):
            cur_url = get_url.format(i)
            page_url.append(cur_url)
            #print 'page_url:',page_url

    temp={}
    kind_title = ""
    #爬取一篇文章的内容
    for article,v in links.items():
        print 'article:',article
        line = get_article(article)
        temp[line] = '1'
        print 'temp:',temp

        kind_title = v
        #防止被封IP
        stop = random.randint(1, 5)
        print 'sleep:',stop
        time.sleep(stop)

    now = time.time()
    day = time.strftime("%Y-%m-%d", time.localtime(now))
    title ='article_' +kind_title+'_' +day + '.txt'
    print 'file:',title
    f = open(title, 'w')
    for line,v in temp.items():
        if( len(line) > 0):
            f.write(line+'\n')
            f.flush()
    print 'get url:',url

#sudo pip install BeautifulSoup4 lxml
    while True:
        #爬取一个分类的文章
        for url, v in kind_url.items():
            pos = url.find('/kind/')
            if( pos != -1):
                pos1 = url.find('?', pos)
            if( pos1 != -1):
                kind = url[pos+len('/kind/'):pos1-1]
            print 'current kind:',kind

            get_kind(kind, v);

    time.sleep(600)

