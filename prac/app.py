#-*- encoding: utf-8 -*-

from flask import Flask, render_template, request, jsonify # flask > Flask : 서버 객체를 띄워놓는것 (지휘자)

app = Flask(__name__) # 지휘자의 이름은 app이야

# 1. HTML을 보여주는 영역
@app.route('/') # / 주소로 들어오면 바로 밑에 있는 함수를 실행해
def main_page():
    return render_template('index.html') # render_template으로 쓸 때 temaplates 폴더 안에 있는 index.html 를 찾아서 보여줘

# 2. 데이터를 가공해서 돌려주는 영역 - 직접 데이터를 넣어보자.

@app.route('/test', methods=['GET'])
def test_get():
    received = request.args.get('title_give')
    # request.args.get : user가 나에게 보낸 요청에 title_give라고 되어 있는 arguments(구성요소) 불러와
    # (request의 구성 요소(args)들 중에 title_give에 달린 정보를 가져와줘)
    print(received)

    # jsonify : json 형식으로 만들어서 (인코딩 문제) 아래 딕셔너리를 보내줘
    return jsonify({
        'result' : 'success',
        'msg' : '이 요청은 GET!이었네요!'
    })

@app.route('/test', methods=['POST'])
def test_post():
    received = request.form['title_give']
    print(received)

    return jsonify({
        'result' : 'success',
        'msg' : '이 요청은 Post 입니다!'

    })

@app.route('/sample')
def show_sample():
    return '여기는 샘플 사이트 입니다!'

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
