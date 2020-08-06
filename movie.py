import requests
from bs4 import BeautifulSoup
import csv

###########################################
########### 영화 제목 & 코드 ###############
###########################################

response = requests.get('https://movie.naver.com/movie/running/current.nhn')
movie_code_soup = BeautifulSoup(response.text, 'html.parser')

movies_list = movie_code_soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li')

final_movies_list = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag['href'].split('code=')[1] #movie_code[movie_code.find('code=') + len('code='):]
    
    movie_data = {
        'title' : movie_title,
        'code' : movie_code
    }

    final_movies_list.append(movie_data)
# print(final_movies_list)

###########################################
############### csv 저장 ##################
###########################################

# with open ('movie.csv', 'a', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=['name', 'code'])
#     writer.writerow(movie_data)


###########################################
########### 영화 리뷰 & 평점 ###############
###########################################



for movie in final_movies_list:
    movie_code = movie['code']
    # print(movie_code)

    params = (
        # 코드를 변수로 바꿔주기
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    # response는 html
    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=189069&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false', headers=headers)


    review_soup = BeautifulSoup(response.text, 'html.parser')

    #review의 html에 들어가서 구조 확인
    review_list = review_soup.select(
        'body > div > div > div.score_result > ul > li'
    )

    count = 0
    for review in review_list:
        score = review.select_one('div.star_score > em').text 
        reple = ''

        if review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}') is None:
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count}').text.strip()
        # 리뷰가 긴 경우 처리
        elif review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}'):
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count} > span > a')['data-src']


        print(score, reple, sep='\n')

        count += 1