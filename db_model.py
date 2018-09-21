# -*- coding:UTF-8 -*-
from mongoengine import *


class DongWu(Document):
    """冬吴实例"""
    title = StringField(required=True)
    audio_url = StringField(required=True)

    meta = {
        'collection': 'Dongwu',
    }


class DongWu_Mongo(object):
    def __init__(self):
        connect('ximalaya')

    def add_one(self, title, audio_url):
        """添加一条数据到数据库"""
        DongWu_obj = DongWu(
            title=title,
            audio_url=audio_url
        )
        DongWu_obj.save()
        return DongWu_obj

    def get_one(self):
        """查询一条数据"""
        return DongWu.objects.first()

    def get_more(self):
        """查询多条数据"""
        return DongWu.objects.all()

    def get_from_oid(self, oid):
        """根据ID来获取数据"""
