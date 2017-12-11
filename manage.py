# -*- coding: utf-8 -*-
import argparse
__author__ = 'wataru'


if __name__ == '__main__':
    #エラーの時にメッセージを表示する。 
    parser = argparse.ArgumentParser("Runner")
    parser.add_argument('action', type=str, nargs=None, help="Select target 'crawler' or 'webpage'?")
    args = parser.parse_args()

    if args.action == 'crawler':
        #コマンドラインでcrawlerって打ち込まれたらweb_crawlerって言うフォルダからcrawler.pyを読み込んでcrawl_webっていうdefを持ってくる    
        from web_crawler.crawler import crawl_web
        crawl_web('https://www.aasa.ac.jp/', 15)
    elif args.action == 'webpage':
        from search_engine import app
        app.run(debug=True, host='0.0.0.0', port=9000)
    elif args.action == 'dropdb':
        from web_crawler.drop_collection import drop_collection
        drop_collection()
    else:
        raise ValueError('Please select "crawler" or "webpage" or "dropdb".')
