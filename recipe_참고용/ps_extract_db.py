#-*- encoding: utf-8 -*-


from pymongo import MongoClient

#client 인증
client = MongoClient('localhost', 27017) #인증
db = client.dbsparta # 이 선반을 쓸거야!

# 1. 데이터 하나 가져오기
# db 컨테이너 > movies 선반 > '월-E' 하나 찾아와(find_one).
# find_one: 하나 찾아와 find: 다 찾아와
target_movie = db.movies.find_one({
    'title' : '월-E'
})

# print(target_movie)

# 2. 데이터 여러개 가져오기
# db 컨테이너에서 movies 선반에서, star가 standard_star 인 영화를 가져와
# > list로 감싸야 python에서 인식할 수 있는 형태로 가져오는 것.
standard_star = target_movie['star'] # 9.41
selected_movies = list(db.movies.find({'star': standard_star}))

# print (selected_movies)

# 3. 데이터 덮어쓰기
# 업데이트 할 대상. 'star': standard_star
# $set: 어떻게 바꿔줄지 명령어 후 {} 안에 어떻게 바꿀 지 써

db.movies.update_many(
    {'star': standard_star},
    {'$set': { # 이렇게 설정하시오!
        'star': 0 # 골라진 'star'를 0으로 만들어라!
     }}
)

print (selected_movies)

