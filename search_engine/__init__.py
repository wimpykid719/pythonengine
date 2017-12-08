from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from web_crawler.crawler import crawl_web

app = Flask(__name__)
app.config.from_object('config') #flaskのconfigを読み込んでる

# DB settings
MONGO_URL = app.config['MONGO_URL']
client = MongoClient(MONGO_URL)
db = client[urlparse(MONGO_URL).path[1:]]
col = db["Index"]
col2 = db["Webname"]

# DB col + col2




@app.route('/', methods=['GET', 'POST']) #postはフォームにキーワードぶち込んでDBに探させる時
def index():
    """Return index.html
    """
    if request.method == 'POST':
        keyword = request.form['keyword'] #フォームで入力された文字がkeyword変数に入っているのでそれを持ってくるそこからkeywordに代入
        if keyword:
            if keyword == 'wataru':
                return redirect(url_for('crawler'))
            url_and_title = []
            url_and_keyword_field = col.find_one({'keyword': keyword})
            if url_and_keyword_field:
                urls = url_and_keyword_field['url']
                for url in urls:
                    title_field = col2.find_one({'url':url})
                    if title_field:
                        title = title_field['title']
                        url_and_title.append([title, url])
                    else:
                        url_and_title.append([url, url])
            return render_template(
                'result.html',
                query=url_and_title,
                keyword=keyword)
    return render_template('index.html')

@app.route('/crawler', methods=['GET', 'POST'])
def crawler():
    """seacretpage
    """
    crawled = []
    if request.method == 'POST':
        url = request.form['url'] #フォームで入力された文字がkeyword変数に入っているのでそれを持ってくるそこからkeywordに代入
        if 'http' in url:
                crawled = crawl_web(url, 0)
                return render_template(
                    'done.html',
                    crawled=crawled,
                    url=url)
                
    return render_template('crawler.html')

#DBにこんな感じでデータが入ってる。pythonでいう辞書型
# { "_id" : ObjectId("59c76e3495babe084f1e23eb"), "keyword" : "Home", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23ec"), "keyword" : "Get", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23ed"), "keyword" : " ", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23ee"), "keyword" : "it", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23ef"), "keyword" : "Docs", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23f0"), "keyword" : "Extend", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23f1"), "keyword" : "/", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3495babe084f1e23f2"), "keyword" : "Develop", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3895babe084f1e23f3"), "keyword" : "ナビゲーション", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3895babe084f1e23f4"), "keyword" : "索引", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23f5"), "keyword" : "モジュール", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23f6"), "keyword" : "|", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23f7"), "keyword" : "次", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23f8"), "keyword" : "へ", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23f9"), "keyword" : "Sphinx", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23fa"), "keyword" : "home", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23fb"), "keyword" : " ", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23fc"), "keyword" : "Documentation", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3995babe084f1e23fd"), "keyword" : "»", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }
# { "_id" : ObjectId("59c76e3c95babe084f1e23fe"), "keyword" : "目次", "url" : [  "http://docs.sphinx-users.jp/contents.html" ] }