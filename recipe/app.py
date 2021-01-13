import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from bs4.element import NavigableString

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(
    'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=&cat3=70&cat4=56&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=',
    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
recipes = soup.select('#contents_area_full > ul > ul > li')
# print(recipes)
for recipe in recipes:
    # xx.select_one: 여러가지 중 하나만 잡는 것 (맨 처음 하나)
    # td.title: td에 class 이름이 title로 달려있는 거
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
        recipe_steps = recipe_soup.select('#contents_area > div.view_step > div.view_step_cont')
        # recipe_step_text = recipe_steps[i].text
        print(recipe_steps)
        recipe_steps_soup = BeautifulSoup(recipe_steps, 'html.parser')

        for bs_object in recipe_steps_soup:
            print("[object]", type(bs_object))
            print("[repr]")
            print(bs_object)
            print("-----")