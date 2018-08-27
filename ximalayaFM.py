# -*- coding:utf-8 -*-
"""利用request爬取喜马拉雅FM里‘冬吴同学会’专辑所有音频
    实现 1.下载音频到本地
        2. 将json中重要信息（url接口等等）存在mongodb数据库
    __author__ = 'LuyiBuddha'
"""
import os

import requests
from lxml import etree
import sys
#import db_model

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


def get_audio():
    title = u'冬吴同学会'
    start_url = 'http://www.ximalaya.com/83432108/album/8475135/'
    response = requests.get(start_url, headers=headers).text
    print 'response:',response
    num_list = etree.HTML(response).xpath('//div[@class="personal_body"]/@sound_ids')[0].split(',')
    mkdir(title)
    os.chdir(r'./ximalayaFM/' + title)
    for id in num_list:
        json_url = 'http://www.ximalaya.com/tracks/{}.json'.format(id)
        html = requests.get(json_url, headers=headers).json()
        print html
        audio_url = html.get('play_path')
        title = html.get('title')
        download(audio_url, title)
        #dm.add_one(title, audio_url)
        print '{0}, 下载和加入数据库完毕'.format(title)


def mkdir(title):
    path = './ximalayaFM/'
    isExists = os.path.exists(os.path.join(path, title))
    if not isExists:
        print (u'创建一个名子叫做{}的文件夹'.format(title))
        os.makedirs(os.path.join(path, title))
        return True


def download(url, title):
    title = title + '.m4a'
    content = requests.get(url).content  # 返回的是二进制（常用于图片，音频，视频）
    with open(title, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    #dm = db_model.DongWu_Mongo()
    get_audio()

    # rows = dm.get_more()
    # for row in rows:
    #     print row.title + ',' + row.audio_url
