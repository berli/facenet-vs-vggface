# -*- coding: utf8 -*-)
import json
import re
import os
import requests

class Xima(object):
    def __init__(self, book_id, book_name):
        # 保存文字用的
        self.book_name = book_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        # 当前书的第一页的url, 把书的id留着就是为了咱们能够更方便的获取别的书的音频信息
        self.start_url = "https://www.ximalaya.com/revision/play/album?albumId=%s&pageNum={}&sort=-1&pageSize=30" % book_id
        # 当前书的每一页的url
        self.book_url = []
        for i in range(8):  # 如果想获得准备的多少页, 可以从第一页里面把多少页的信息找到, 然后放到range()里面
            url = self.start_url.format(i + 1)
            self.book_url.append(url)
            # print(self.book_url)


    def get_book_msg(self):
        """获取到所有书的音频信息和书名"""
        all_list = []  # 存储当前书的所有音频和书名信息
        for url in self.book_url:
            # 遍历每一页的url, 从中提取每一页的音频数据
            r = requests.get(url, headers=self.headers)
            #python_dict = json.loads(r.content.decode())  # 得到第一页的所有书的字典数据
            python_dict = json.loads(r.content)  # 得到第一页的所有书的字典数据
            book_list = python_dict['data']['tracksAudioPlay']  # 第一页的所有书信息, 所有音频对应到的当前层次字典
            for book in book_list:
                # 遍历取出每一个音频的播放地址信息和名字放进字典
                list = {}
                list['src'] = book['src']
                list['name'] = book['trackName']
                # 所有单个音频都放进列表当中
                all_list.append(list)
        print(all_list)
        return all_list

    def save(self, all_list):
        """保存每一本书到本地"""
        # 遍历每一个音频, 然后保存
        local = self.getLocal();
        #for k,v in  local.items():
        #    print k
        for i in all_list:
            print(i)
            # {'src': 'http://audio.xmcdn.com/group44/M01/67/B4/wKgKkVss32fCcK5xAIMTfNZL0Fo411.m4a', 'name': '到日本投资民宿还能挣钱吗？'}
            i['name'] = re.sub('"', '', i['name'])  # 有些名字里面会带有", 这个时候, 因为转义的问题, 程序会报错, 所有我们得把"替换成空白,
            fname = self.book_name + i['name'].encode('utf-8')
            fname = fname+'.m4a'
            print fname
            if(fname in  local):
                print '已经下载'
                continue;

            with open(r'xima/{}.m4a'.format(self.book_name + i['name'].encode('utf-8')), 'ab') as f:
                print 'downloading:',self.book_name + i['name'].encode('utf-8')
                r = requests.get(i['src'], headers=self.headers)
                ret = r.content
                # 获取到音频的二进制文件保存起来才是音频文件
                f.write(ret)

    def getLocal(self):
        files = os.listdir('xima')
        flist = {}
        for file in files: #遍历文件夹
            if not os.path.isdir(file): #判断是否是文件夹
                flist[file] = "";

        return flist;

    def run(self):
        """运行方法"""
        all_list = self.get_book_msg()
        self.save(all_list)


if __name__ == '__main__':
    # 传进去当前书的json id, 才能得到正确的json数据
    #xima = Xima('16861863', '冬吴同学会')
    xima = Xima('8475135', '冬吴同学会')
    xima.run()
