from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

@app.route('/')
def home():
    return render_template('index.html')
# 2. 데이터 어떻게 주고받지?
# 2a. URL을 받아서 > meta 정보를 긁고 > DB에 저장
@app.route('/memo', methods=['POST'])
def post_articles():
    url_received = request.form['url_give']
    comment_received = request.form['comment_give']

    # print(url_received)
    # print(comment_received)

    # 1. URL을 가지고, meta 태그 크롤링해서 필요한 정보 뽑아 (아래는 복사함)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_received, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    # 아래는 원리가 어떻게 되는지 알 필요는 없음.
    url_title = og_title['content']
    url_description = og_description['content']
    url_image = og_image['content']

    # 3. container로 묶어
    container = {
        'url' : url_received, # 내가 받은 URL
        'title' : url_title, # 크롤링한 제목
        'desc' : url_description, # 크롤링한 desc
        'image' : url_image, # 크롤리안 이미지
        'comment' : comment_received # 내가 받은 댓글
    }

    # 4. DB에 넣어주면 되겠다!
    db.articles.insert_one(container)

    return jsonify({
        'result': 'success',
        'msg': 'POSt 통신!'
    })

# 2b. 페이지가 로딩되면 > DB에서 정보 긁어서 보여줘
@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. DB에 있는거 긁고
    result = list(db.articles.find({}, {'_id':0})) # {} : 싹다 찾고, /{'_id':0}: id는 주지마
    print(result)
    # 2. 정리해서 보내주자!
    return jsonify({
        'result' : 'success',
        'articles' : result,
        'msg' : 'GET 통신!'
    })




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
