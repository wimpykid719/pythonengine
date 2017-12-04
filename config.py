import os

#接続先のホストはデフォルトだと ‘localhost’ でポート番号は 27017
# application settings
#os.environ.get('MONGO_URL')通常のサーバーにアプリをあげるならこのようにしてURLを持ってくる必要があると思う。
MONGO_URL = 'mongodb://localhost:27017/test'
#MONGO_URL2 = 'mongodb://localhost:27017/name'
# Generate a random secret key
SECRET_KEY = os.urandom(24)
#セキュリティについての設定だけどxssとcsrfというのがあるらしい（多分使われてないけど聞く必要がある）
#flaskのconfig設定だと思ったけど違った。
CSRF_ENABLED = True