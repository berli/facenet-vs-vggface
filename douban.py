
# -*- coding: utf-8 -*-)
import urllib2
import time
from bs4 import BeautifulSoup
import sys
import random
reload(sys) 
sys.setdefaultencoding('utf-8')

def get_article_link(url):

    response = urllib2.urlopen(url)
    res = response.read()
    bsObj = BeautifulSoup(res, 'html.parser')
    links = bsObj.find_all('a')
    articles = {}
    max = 0;
    for link in links:
        l = str(link.get('href'))
        #print 'links:',l
        #print 'urls:',urls
        #print 'type(l):',type(l)
        if( l.find('/ebook/') == 0):
            articles['https://read.douban.com/'+l]='1'
        if( l.find('https://read.douban.com/column/') == 0):
            articles[l] = "1"
        elif( l.find('?start=') == 0):
            pos = l.find('?start=')
            pos1 = l.find('&', pos)
            if( pos1  != -1):
                start = l[pos+len('?start='):pos1]
                if( int(start) > max):
                    max = int(start)
                print start
                print l

    return articles, max

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

    if( not special):
        for read in  bsObj.find_all('span', class_='read-count'):
            print 'read-count:', read.text.split()[0]
            line += read.text.split()[0];
            line +=','
    else:
        #专栏
        special_count = 0;
        for read in  bsObj.find_all('span', class_='count'):
            cnt = int(read.text.replace(',',''))
            if(cnt > special_count):
                special_count = cnt
        line += str(special_count)
        line +=','
        print 'specail read-count:', special_count

    flag = False
    for read in  bsObj.find_all('span', class_='score'):
        line += read.text
        line +=','
        print 'score:', read.text
        flag = True;
    if(len(line) > 0 and not flag):
        line +=','

    for read in  bsObj.find_all('span', class_='amount'):
        print 'rating:', read.text.split()[0]
        line += read.text.split()[0]

    return line

if __name__ == '__main__':

    url = "https://read.douban.com/kind/532?start=0&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    get_url = "https://read.douban.com/kind/532?start={0:d}&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None"
    
    links,max = get_article_link(url)
    page_url =[]
    
    if( max > 20):
        for i in range(20, max, 20):
            cur_url = get_url.format(i)
            page_url.append(cur_url)
            #print 'page_url:',page_url


    now = time.time()
    day = time.strftime("%Y-%m-%d", time.localtime(now))
    title ='article_' + day + '.txt'

#sudo pip install BeautifulSoup4 lxml
    f = open(title, 'w')
    while True:
        for url in page_url:
            temp={}
            for article,v in links.items():
                print 'article:',article
                line = get_article(article)
                temp[line] = '1'
                print 'temp:',temp

                #防止被封IP
                stop = random.randint(2,10)
                print 'sleep:',stop
                time.sleep(stop)

            for line,v in temp.items():
                if( len(line) > 0):
                    f.write(line+'\n')
                    f.flush()
            print 'get url:',url
            links,max = get_article_link(url)

        time.sleep(24*3600)

