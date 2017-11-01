import requests
import re
from bs4 import BeautifulSoup
#とりあえずaタグの周りを外してurlだけ取り出せるようにして
# r = requests.get('https://www.google.co.jp/')
# html = r.text
# body_soup = BeautifulSoup(html, "html.parser").find('body')
# print(body_soup)

# for child_tag in body_soup.findChildren():
#     print(child_tag)
# 	return

#python 仮想環境入る時 mkvirtualenv dev --python=/usr/bin/python3

r = requests.get('http://ltomu.minibird.jp/')
html = r.text
child_text = []
#print(html)
def takeurl(aurl):
    body_soup = BeautifulSoup(html, "html.parser").find('body')
    for child_tag in body_soup.findChildren():
        
        #beautifulsoupの機能でタグの名前だけ取り出してる。スクリプトだけは避ける。それ以降の処理がスキップされてループに戻る
        if child_tag.name == 'script': #child_tag.nameタグの名前を取り出す
            continue
        #.textはそのタグの中身を表示する。<a>link</a>だったらlinkだけとりだす。
        if child_tag.get('href') is not None:
            if '#' not in child_tag.get('href'):
                child_text.append(child_tag.get('href'))
    print(child_text)
        

def _extract_url_links(html):
    """extract url links

    >>> _extract_url_links('aa<a href="link1">link1</a>bb<a href="link2">link2</a>cc')
    ['link1', 'link2']
    """
    #"html.parser"はなるべくpython標準のparserモジュールを使うように指定しているBeautifulSoup()で
    #BeautifulSoupで扱えるようにしている。

    soup = BeautifulSoup(html, "html.parser")
    #aタグを全て持ってくる。
    #return soup.find_all('a')
    #print(soup.find_all(href=re.compile("http"))) #からの[]が帰ってきた。
    return soup.find_all('a')

aurl = (_extract_url_links(html))
takeurl(aurl)