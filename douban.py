
# -*- coding: utf-8 -*-)
import urllib2
import time
from bs4 import BeautifulSoup
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

def get_article_link(url):

    response = urllib2.urlopen(url)
    res = response.read()
    bsObj = BeautifulSoup(res, 'html.parser')
    links = bsObj.find_all('a')
    articles = []
    max = 0;
    for link in links:
        l = str(link.get('href'))
        #print 'links:',l
        #print 'urls:',urls
        #print 'type(l):',type(l)
        if( l.find('/ebook/') == 0):
            articles.append('https://read.douban.com/'+l)
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
    for read in  bsObj.find_all('span', class_='read-count'):
        print 'read-count:', read.text.split()[0]
        line += read.text.split()[0];
        line +=','

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

    f = open('article.txt', 'w')
    while True:
        for url in page_url:
            temp={}
            for article in links:
                print 'article:',article
                line = get_article(article)
                temp[line] = '1'
                print 'temp:',temp

            for line,v in temp.items():
                if( len(line) > 0):
                    f.write(line+'\n')
            print 'get url:',url
            links,max = get_article_link(url)

        time.sleep(24*3600)

