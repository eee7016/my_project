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
noodle = 53
rice = 52
# 소고기(cat3=70)
# 돼지고기(cat3=71)
# 닭고기(cat3=72)
# 메인반찬(cat4=56)
# 밑반찬(cat4=63)
# 국/탕(cat4=54)
# 찌개(cat4=55)
# 면/만두(cat4=53)
# 밥/죽/떡(cat4=52)
# 소고기(cat3=70) + 메인반찬(cat4=56)
# https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=56&order=reco&page=1
# 소고기(cat3=70) + 밑반찬(cat4=63)
# https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=63&order=reco&page=1
# 소고기(cat3=70) + 국/탕(cat4=54)
# https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=54&order=reco&page=1
# 소고기(cat3=70) + 찌개(cat4=55)
# https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=55&order=reco&page=1
# 소고기(cat3=70) + 면/만두(cat4=53)
# # https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=53&order=reco&page=1
# 소고기(cat3=70) + 밥/죽/떡(cat4=52)
# https://www.10000recipe.com/recipe/list.html?cat3=70&cat4=52&order=reco&page=1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
test_url = 'https://www.10000recipe.com/recipe/list.html?cat3={}&cat4={}&order=reco'.format(cow, noodle)
# client로서 DB에 들어가서 localhost인 내컴퓨터로 27017 로 들어가는 것. 신원 확인
client = MongoClient('localhost', 27017)
db = client.myproject  # myproject = 선반 이름

# 페이지 넘버 넘기는 크롤링 참고 페이지: https://yceffort.kr/2018/11/05/web-crwaling-for-naver-movie
data = requests.get(test_url, headers=headers)
soup = BeautifulSoup(data.content, 'html.parser')
result = soup.select_one('#contents_area_full > ul > div > b').text
print(result)
total_count = int(result.replace(',', ''))

for i in range(1, int(total_count / 40) + 2):
    url = test_url + '&page=' + str(i)
    print('url: "' + url + '" is parsing....')
    recipes = soup.select('#contents_area_full > ul > ul > li')
    for recipe in recipes:
        div_tag = recipe.select_one('div.common_sp_caption > div.common_sp_caption_tit')
        if div_tag == None:
            pass
        else:
            ###############
            # 1. 요리 제목 #
            ###############
            title = div_tag.text  # title
            print(title)
            url = recipe.select_one('div.common_sp_thumb > a')['href']
            full_url = 'https://www.10000recipe.com' + url
            print('full_url: ', full_url)
            recipe_data = requests.get(full_url, headers=headers)
            recipe_soup = BeautifulSoup(recipe_data.text, 'html.parser')
            # Total ingredients: # divConfirmedMaterialArea
            main_ingre = recipe_soup.select('#divConfirmedMaterialArea > ul:nth-of-type(1) > a > li')

            #################
            # 2. 요리 사진 #
            #################
            main_img = recipe_soup.select_one('#main_thumbs')['src']
            print('main_img: ', main_img)

            ###########
            # 3. X인분 #
            ###########
            # div_tag = recipe.select_one('div.common_sp_caption > div.common_sp_caption_tit')
            try:
                serving = recipe_soup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info1').text
            except AttributeError:
                serving = 'None'
            print('servings: ', serving)

            ##############
            # 4. 소요 시간 #
            ##############
            try:
                cooktime = recipe_soup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info2').text
            except AttributeError:
                cooktime = 'None'
            print('cooktime:', cooktime)
            # mongoDB에 넣어주기
            # doc = {
            #     'title' : title,
            #     'main_img' : main_img,
            #     'servings' : serving,
            #     'cooking_time' : cooktime,
            # }
            # db.recipetrial.insert_one(doc)

            ###########################################################
            # 5. MAIN INGREDIENTS: 예쁘게 재료 정보를 추출해주는 크롤링 코드 #
            ###########################################################
            for ingredient in main_ingre:
                ingre_container = []  # ingredient 정보를 넣어줄 공간
                ingre_name = ingredient.text
                ingre_name = ingre_name.split('\n')  # ['차돌박이                                                        ', '10장', '']

                for ingre in ingre_name:
                    cleaned_ingre = ingre.strip()  # strip: 띄어쓰기 삭제!
                    ingre_container.append(cleaned_ingre)
                ingre_container = ingre_container[:2]
                print(ingre_container)
                # mongoDB에 넣어주기
                # doc = {
                #     'main_ingre': ingre_container[0],
                #     'main_ingre_unit': ingre_container[1],
                # }
                # db.recipetrial.insert_one(doc)

            ###############################
            # 6. SIDE INGREDIENTS 추출하기 #
            ###############################
            side_ingre = recipe_soup.select('#divConfirmedMaterialArea > ul:nth-of-type(2) > a > li')
            try:
                side_name = recipe_soup.select('#divConfirmedMaterialArea > ul:nth-of-type(2) > b')[0] #리스트 형태로 끌어오기 리스트 안의 텍스트를 끌어올 수 없음. 그래서 다시 리스트에서 꺼내주는 과정이 필요.
                side_name = side_name.text[1:-1] #중괄호 없애기
            except IndexError:
                side_name = 'None'
            print(side_name)
            # mongoDB에 넣어주기
            # doc = {
            #     'side': side_name,
            # }
            # db.recipetrial.insert_one(doc)

            for ingredient in side_ingre:
                side_ingre_container = []
                side_ingre_name = ingredient.text
                side_ingre_name = side_ingre_name.split('\n')  # ['차돌박이                                                        ', '10장', '']

                for ingre in side_ingre_name:
                    cleaned_ingre = ingre.strip()  # strip: 띄어쓰기 삭제!
                    side_ingre_container.append(cleaned_ingre)
                side_ingre_container = side_ingre_container[:2]
                print(side_ingre_container)
                # mongoDB에 넣어주기
                # doc = {
                #     'side_ingre': side_ingre_container[0],
                #     'side_ingre_unit': side_ingre_container[1],
                # }
                # db.recipetrial.insert_one(doc)

            ################################
            # 7. 추가 INGREDIENTS 추출하기 #
            ################################
            add_side_ingre = recipe_soup.select('#divConfirmedMaterialArea > ul:nth-of-type(3) > a > li')
            try:
                add_side_name = recipe_soup.select('#divConfirmedMaterialArea > ul:nth-of-type(3) > b')[0] #리스트 형태로 끌어오기 리스트 안의 텍스트를 끌어올 수 없음. 그래서 다시 리스트에서 꺼내주는 과정이 필요.
                add_side_name = add_side_name.text[1:-1] #중괄호 없애기
            except IndexError:
                add_side_name = 'None'
            print('add_side: ', add_side_name)
            # mongoDB에 넣어주기
            doc = {
                'additional_side': add_side_name,
            }
            db.recipetrial.insert_one(doc)

            for ingredient in add_side_ingre:
                add_side_ingre_container = []
                add_side_ingre_name = ingredient.text
                add_side_ingre_name = add_side_ingre_name.split('\n')  # ['차돌박이                                                        ', '10장', '']

                for ingre in add_side_ingre_name:
                    cleaned_ingre = ingre.strip()  # strip: 띄어쓰기 삭제!
                    add_side_ingre_container.append(cleaned_ingre)
                add_side_ingre_container = add_side_ingre_container[:2]
                print(add_side_ingre_container)
                # mongoDB에 넣어주기
                # doc = {
                #     'add_side_ingre': add_side_ingre_container[0],
                #     'add_side_ingre_unit': add_side_ingre_container[1],
                # }
                # db.recipetrial.insert_one(doc)

            ###################
            # 8. RECIPE STEPS #
            ###################
            recipe_steps = recipe_soup.select('#contents_area > div.view_step > div.view_step_cont')
            # print(recipe_steps)
            print(len(recipe_steps))

            for i in range(len(recipe_steps)):
                print('Step', i + 1)
                recipe_step_text = recipe_steps[i].text
                recipe_step_text = recipe_step_text.replace("\n", " ")
                print(recipe_step_text)
                try:
                    recipe_step_img = recipe_steps[i].img['src']
                except TypeError:
                    recipe_step_img = 'None'
                print('img: ', recipe_step_img)
                # mongoDB에 넣어주기
                # doc = {
                #     'step' : i + 1,
                #     'recipe': recipe_step_text,
                #     'recipe_img': recipe_step_img,
                # }
                # db.recipetrial.insert_one(doc)


