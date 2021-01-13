from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

#서버를 만져주는 지휘자
app = Flask(__name__)

#DB에 접근하기 위한 기능
client = MongoClient('localhost', 27017)
db = client.dbsparta

###################
# 1. HTML 화면 보여주기
###################
@app.route('/')
def home():
    return render_template('index.html')

##########################
# 2. 데이터를 주고받는 기능, 영역
# 2-1. 새로고침 때리면 알아서 DB에서 정보를 가져와서 알아서 잘 보여줘
# 2-2. 좋아요를 누르면 그 영화 배우의 좋아요 수가 늘어나
# 2-3. 삭제를 누르면 그 영화 배우 정보가 DB에서도 삭제된다
##########################
# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    # 1. db에 저장된 정보를 다 긁어와..
    # 2. 좋아요 순서대로 정렬하자
    # 3. 묶어서 클라에 보내주자
    stars = list(
        db.mystar.find(
        {}, #모든 데이터 가져와! (조건 없이)
        {'_id': False}, #id 더러운 값 필요없어서
    ).sort('like', -1) #like 를 기준으로 내림차순
    )
    print('db를확인합니다')
    print(stars)

    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify(
        {'result': 'success',
         'stars_list': stars}
    )


@app.route('/api/like', methods=['POST'])
def like_star():
    # 1. 유저가 뭘 보냈을까? 확인...
    name_received = request.form['name_give'] # post 방식일 땐 request.form

    # 2. 이름을 기준으로... db에서 찾자 (html의 name_give)
    star = db.mystar.find_one(
        {'name': name_received} #내가 받은 이름과 같은 data를 찾아!
    )

    # 3. like 수 업데이트! 이름 = 유저가 보낸 이름 -> 데이터 ==> 업데이트... like +1
    current_like = star['like']
    new_like = current_like + 1

    # 4. update db... 새로운 값으로 저장...
    db.mystar.update_one(
        {'name': name_received}, #뭐 업데이트 할건데? (대상 데이터)
        {'$set': { #어떻게? 바꿀건데? like 를 new_like로!
            'like': new_like
        }}
    )

    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 유저가 넘겨준 이름 정보 받아.. 유저가 뭘 지우라고 했는지 받고..
    name_received = request.form['name_give']

    # 2. db에서 뭘 지울지 데이터를 찾아.. name 기준으로찾아
    # 3. 지워!
    db.mystar.delete_one(
        {'name': name_received}
    )

    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)