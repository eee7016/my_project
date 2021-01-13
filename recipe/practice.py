import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

cow = 70
pig = 71
chicken = 72
maindish = 56
sidedish = 63
soup = 54
jjigae = 55
rice = 52
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(
#     'https://www.10000recipe.com/recipe/list.html?cat3={}&cat4={}&order=reco&page=1'.format(cow, rice),
#     headers=headers)

# https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=63&order=reco&page=1

# print(data)
# soup = BeautifulSoup(data.text, 'html.parser')
# recipes = soup.select('#contents_area_full > ul > ul > li')
# print(recipes)


test_url = 'https://www.10000recipe.com/recipe/list.html?cat3={}&cat4={}&order=reco'.format(cow, rice)
resp = requests.get(test_url, headers=headers)
html = BeautifulSoup(resp.content, 'html.parser')
result = html.select_one('#contents_area_full > ul > div > b').text
print(result)
total_count = int(result.replace(',', ''))

for i in range(1, int(total_count / 40) + 2):
    url = test_url + '&page=' + str(i)
    print('url: "' + url + '" is parsing....')
#     get_data(url)


# 소고기(cat3=70)
# 돼지고기(cat3=71)
# 닭고기(cat3=72)

# 메인반찬(cat4=56)
# 밑반찬(cat4=63)
# 국/탕(cat4=54)
# 찌개(cat4=55)
# 면/만두(cat4=53)
# 밥/죽/떡(cat4=52)
#
# def get_data(url):
#     resp = requests.get(url)
#     html = BeautifulSoup(resp.content, 'html.parser')
#     score_result = html.find('div', {'class': 'score_result'})
#     lis = score_result.findAll('li')
#     for li in lis:
#         nickname = li.findAll('a')[0].find('span').getText()
#         created_at = datetime.strptime(li.find('dt').findAll('em')[-1].getText(), "%Y.%m.%d %H:%M")
#
#         review_text = li.find('p').getText()
#         score = li.find('em').getText()
#         btn_likes = li.find('div', {'class': 'btn_area'}).findAll('span')
#         like = btn_likes[1].getText()
#         dislike = btn_likes[3].getText()
#
#         watch_movie = li.find('span', {'class':'ico_viewer'})
#
#         # 간단하게 프린트만 했습니다.
#         print(nickname, review_text, score, like, dislike, created_at, watch_movie and True or False)

# test_url = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=136990&type=after&page=1"
# resp = requests.get(test_url)
# html = BeautifulSoup(resp.content, 'html.parser')
# html

