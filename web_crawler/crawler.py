# -*- coding: utf-8 -*-

#pythonの標準のモジュールでurlからhtmlのファイルを持って来てくれる。
import requests
#Python正規表現
import re

#pythonの標準のモジュールでurlの解析をしてくれる。
from urllib.parse import urlparse
#mongodbを操作する時に使用するモジュールでMongoClientでDBに接続する。
from pymongo import MongoClient
#日本語形態のやつを解析できる。
from janome.tokenizer import Tokenizer
#htmlからリンクを抜き出してくれる。
from bs4 import BeautifulSoup
#config.pyからMONGO_URLを持ってくる。
from config import MONGO_URL

#DBに接続
#print(MONGO_URL) mongodb://localhost:27017/test

client = MongoClient(MONGO_URL)
#urlparseでURLのパスだけ抜き出す。それでデータベースを取得
#print(client) MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)

#client[]はpythonの仕様じゃなくてpymongoの仕様、普通はclient.test_databaseでもいいけど'test-database'という
#風に使いたい場合は['test-database']と書くディクショナリ型を使う
db = client[urlparse(MONGO_URL).path[1:]] #.pathによって'/test'が抜き出されるそして[1:]によって前にある/が取り除かれる。
#dbに突っ込むと勝手にDatabase()が付くのも仕様
#print(db) Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'test')
#存在するtestデータベースからIndexというコレクションを取り出す。
col = db["Index"]
#ここでコレクション"Index"を作っている。
#print(col) Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'test'), 'Index')

col2 = db["Webname"]

def split_str_to_500(text):
    """split string by its length janomeが一度に\
    たくさんの英語やら日本語が入ったテキストを送るとエラーが出る\
    のでここで区切ってる。現在はバージョンアップして治っている。"""
    length = len(text)
    return [text[i:i+500] for i in range(0, length, 500)]

def _split_to_word(text):
    """Japanese morphological analysis with janome.
    Splitting text and creating words list.
    """
    t = Tokenizer()
    #token.surfaceで日本語の文字だけ取り出せる。例えば車は高いだったら"車" "は" "高い" だけ取り出せる。
    return [token.surface for token in t.tokenize(text)]


def _get_page(url):
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    #r変数に<!DOCTYPE html>から代入する。
    r = requests.get(url) #, headers=headers
    #レスポンスコードが200で正常だったら文字列""にして返す。
    r.encoding = r.apparent_encoding
    if r.status_code == 200:
        return r.text

def _get_page_tite(html):
    
    title = BeautifulSoup(html, "html.parser").find('title')
    if title:
        return title.text
    else:
        return

def add_to_webname(url, title):
    entry = col2.find_one({'title': title})
    if not entry:
        col2.insert({'url': url, 'title': title})
        return
    # not found, add new keyword to index
    

def _extract_url_links(html, rooturl):
    """extract url links
    >>> _extract_url_links('aa<a href="link1">link1</a>bb<a href="link2">link2</a>cc')
    ['link1', 'link2']
    """
    #"html.parser"はなるべくpython標準のparserモジュールを使うように指定しているBeautifulSoup()で
    #BeautifulSoupで扱えるようにしている。
    root_url = rooturl
    img_suffixes = (".png", ".jpg", ".gif", "pdf")
    all_url = []
    body_soup = BeautifulSoup(html, "html.parser").find('body')
    if body_soup is None:#bodyタグ以下を取得できなければ次のurlをたどる。
        return []
    #aタグを全て持ってくる。
    #print(soup.find_all(href=re.compile("link")))からの[]が帰ってきた。
    #
    for child_tag in body_soup.findChildren():
        if child_tag.get('href') is not None:
            if '#' not in child_tag.get('href'):
                url_parts = urlparse(child_tag.get('href'))#url_parts.fragmentはurl#以降があったらそれは同じページ内移動になるので追加しないそして
                if not url_parts.fragment and not url_parts.path.endswith(img_suffixes):#pathの最後から検索してpngとかがあったら除外する。
                    if url_parts.scheme:
                        all_url.append(child_tag.get('href'))
                    else:
                        all_url.append(root_url + child_tag.get('href'))
    return all_url


def add_to_index(keyword, url):
    #DBからキーワードが含まれたドキュメントを持ってくるentryに代入する
    entry = col.find_one({'keyword': keyword})

    if entry:
        #entryの中にあるurlと引数のurlが同じじゃなければurlに引数のurlを追加して
        if url not in entry['url']:
            entry['url'].append(url)
            #DBに保存する。saveは追加よりも更新って感じ
            col.save(entry)
        return 
        #普通リターンしないとそのまますとんと落ちるだからelseがいる。ループするときは
    # not found, add new keyword to index
    col.insert({'keyword': keyword, 'url': [url]})


def add_page_to_index(url, html):
    body_soup = BeautifulSoup(html, "html.parser").find('body')
    if body_soup is None:#bodyタグ以下を取得できなければ次のurlをたどる。
        return 
    #htmlないの属性タグとその中身をchild_tagに入れていってる<body>以下にある全てのタグ<a>やら<th>やらを持ってくる。
    #先ずはbodyより下のhtml全部持ってきて次にその下のdivを持ってきてul持ってきてどんどん掘り下げる感じ
    #if body_soup.findChildren() is not None:
    for child_tag in body_soup.findChildren():
        #beautifulsoupの機能でタグの名前だけ取り出してる。スクリプトだけは避ける。それ以降の処理がスキップされてループに戻る
        if child_tag.name == 'script': #child_tag.nameタグの名前を取り出す
            continue
        #.textはそのタグの中身を表示する。<a>link</a>だったらlinkだけとりだす。
        child_text = child_tag.text
        for line in child_text.split('\n'): #文字列から改行を取り除いて分ける。
            line = line.rstrip().lstrip() #上のコードだけだと両端の空白が消せないからここで削除している。実際には削除はできないので取り除いたのを返している
            if len(line) > 500:
                short_line = split_str_to_500(line)
                for line in short_line:
                    for word in _split_to_word(line): #janomeで日本語形態解析して単語をwordに代入
                        add_to_index(word, url)
            else:
                for word in _split_to_word(line): #janomeで日本語形態解析して単語をwordに代入
                        add_to_index(word, url)


def crawl_web(seed, max_depth):
    to_crawl = {seed} #urlをto_crawlに入れて
    crawled = []
    next_depth = []
    depth = 0
    while to_crawl and depth <= max_depth:
        #回収したurlの後ろを削除しpage_urlに入れる。
        page_url = to_crawl.pop() #to_crawl（最初はurlが1つしか入らない）からurlを取り出して削除する
        print(page_url)
        if page_url not in crawled:
            html = _get_page(page_url)
            if html:
                title = _get_page_tite(html)
                add_to_webname(page_url, title)
                add_page_to_index(page_url, html)
                to_crawl = to_crawl.union(_extract_url_links(html, page_url)) #to_crawlに今まで入ってたurlとbf4で持ってきたurlを足してto_crawlに戻す最初0 + 5、4 + 2、5 + 0
                #ここでaタグからurlだけ取り出す。to_crawlには<a>のついたurlのリストが入ってくる
                # print(to_crawl) #to_crawlは空だったset()
                crawled.append(page_url)
        if not to_crawl:
            to_crawl, next_depth = next_depth, [] #next_depthいる？
        depth += 1
    return to_crawl
