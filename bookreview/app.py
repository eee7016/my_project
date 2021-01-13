#-*- encoding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

### Step 1. 서버, DB에 접근할 요소들을 미리 정의
# 1. 서버의 지휘자
app = Flask(__name__)

# 2. DB 어떻게 들어갈건데?
client = MongoClient('localhost', 27017) # 27017 앞 컨테이너에 설거야
db = client.dbsparta

### Step 2. 본격적으로 서버 짜기

# 1. HTML을 넘겨서 보여주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# 2. 필요한 기능을 정의하는 부분
# 2a. 리뷰를 쓰고, DB에 저장시키는 개념(POST)
@app.route('/review', methods=['POST'])
def write_review():
    # 클라가 보내준 데이터를 잘 가공해서 저장
    # 1. 클라(index.html)가 넘겨준 데이터 확인
    title_received = request.form['title_give']
    author_received = request.form['author_give']
    review_received = request.form['review_give']

    # 아래 실행 해보고 cmd 에서 결과값이 나오는지 확인. > 결과값 나옴!
    print(title_received)
    print(author_received)
    print(review_received)

    # 2. DB에 넣어줘!
    container = {
        'title' : title_received,
        'author' : author_received,
        'review' : review_received
    }

    # 3. DB에 넣어주기
    db.reviews.insert_one(container)

    return jsonify({
        'result' : 'success',
        'msg' : '성공적으로 POST를 수행했습니다!'
    })
# 2b. DB에서 리뷰룰 가져와서 클라이언트(html)에게 전달하는 개념(GET)
@app.route('/review', methods=['GET'])
def read_review():
    # DB에서 싹 다 가져온 정보를 reviews에 저장!
    reviews = list(db.reviews.find({}, {'_id':0}))  # '_id:0' _id 가 0이면 가져오지 마

    return jsonify({
        'result' : 'success',
        'msg' : '성공적으로 GET을 수행했습니다!',
        'reviews' : reviews
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)