#-*- encoding: utf-8 -*-

# import requests #request라는 라이브러리 쓸거야
# #requests라는 라이브러리에 있는 get이라는 기능을 써서 url에 있는 데이터를 가져와서 rm
# #그 결과를 response_data에 붙여줘
# response_data = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
# cityair = response_data.json() #json: 예쁘게 데이터만 추려줘
#
# selected_list = cityair['RealtimeCityAir']['row']
# print(selected_list[0])
# # print(cityair['RealtimeCityAir'])
# # print(cityair['RealtimeCityAir']['RESULT'])
# # print(cityair['RealtimeCityAir']['RESULT']['CODE'])
#

# requests 는 기능이 많이 없어서 바로 import requests 쓰면 돼
# 하지만 기능이 많은 라이브러리는 from xxx import xxx 이렇게




# 1. 필요한 라이브러리를 정의
import requests
from bs4 import BeautifulSoup

# 1-B. DB 관리에 필요한 라이브러리인 pymongo
from pymongo import MongoClient


# 2. 타겟 페이지에서 데이터 가져오기
# 외부에서 가져오는 인증서같은 ... 그래서 그냥 복붙으로.
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200716', headers=headers)

# 2-B. 타겟 페이지에서 데이터 가져오기
# client로서 DB에 들어가서 localhost인 내컴퓨터로 27017 로 들어가는 것. 신원 확인
client = MongoClient('localhost', 27017)
# 내가 원하는 db 안에서의 선반 이름은 dbsparta라는 선반으로 가.
db = client.dbsparta # dbsparta = 선반 이름


# 4. 읽은 데이터를, html 문법에 맞게 다시 읽고, soup에 넣어준다!
# data.text: data의 text만 가져올거야.
# BeautifulSoup() 안에 넣으면 그 soup 안에 넣어줘
# html.parser: html 파일이니 그걸 문법으로 읽어줘

soup = BeautifulSoup(data.text, 'html.parser')

#원하는 거만 떠보자! => 가장 가까운 부모부터 파고 들어간다
#soup.select: soup에서 원하는 것만 골라.
# '#old_content' old_content라는 id를를가진 애한테 가
movies = soup.select('#old_content > table > tbody > tr')

for movie in movies:
    #xx.select_one: 여러가지 중 하나만 잡는 것 (맨 처음 하나)
    #td.title: td에 class 이름이 title로 달려있는 거
    a_tag = movie.select_one('td.title > div > a')
    if a_tag == None:
        pass
    else:
        #a_tag.text: 그 중 데이터에 text만 가져와
        title = a_tag.text #title
        rank = movie.select_one('td.ac > img')['alt']
        star = movie.select_one('td.point').text

        pocket = {
            'title' : title,
            'rank' : rank,
            'star' : star

        }
        db.movies.insert_one(pocket)
        print('[DB알림]', title, '데이터를 성공적으로 저장했습니다!')

# dbsparta 의 컨테이너가 있는데 그중 하나의 선반으로 movies 에 가서 pocket 데이터를 insert one 할 예정.

