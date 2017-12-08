# -*- coding: utf-8 -*-

#これを直接実行するとDBの中身が削除される。


#help()でやると作った人の名前で出る。

__author__ = 'Wataru'

#web_crawlerからDBのデータを持ってくるそしてcolの中にしまっとく。
from urllib.parse import urlparse
from pymongo import MongoClient
from config import MONGO_URL



client = MongoClient(MONGO_URL)
db = client[urlparse(MONGO_URL).path[1:]]
# col = db["Index"]
col = db["Index"]
col2 =db["Webname"]

def drop_collection():
	#作成したDBのコレクションを削除する。	
    col.drop()
    col2.drop()

#if__name__ == '__main__'はこれが直接実行されたものなのか(python drop_collection.py)チェックしてもしそうなら
#drop_collectionを実行する。
if __name__ == '__main__':
    drop_collection()
