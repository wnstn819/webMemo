import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.kraft

# MongoDB에 insert 하기

# 'users'라는 collection에 {'name':'bobby','age':21}를 넣습니다.
# db.users.insert_one({'name':'bobby','age':21})
# db.users.insert_one({'name':'kay','age':27})
# db.users.insert_one({'name':'john','age':30})
# 'users' collection 삭제
# db.users.drop()


# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')


movies = soup.select('.list_ranking > tbody > tr')
# movies (tr들) 의 반복문을 돌리기
db.movies.drop()
for movie in movies:
    # movie 안에 a 가 있으면,
   
    a_tag = movie.select_one('td.title > div > a')

    if a_tag is not None:
        # a의 text를 찍어본다.
        a_rank = movie.select_one(' td:nth-child(1) > img')["alt"]
        a_point = movie.select_one('td.point')
        doc = {
            'rank' : a_rank,
            'title' : a_tag.text,
            'star' : a_point.text
        }
        db.movies.insert_one(doc)
        


target_movie = db.movies.find_one({'title' : '매트릭스'})
print(target_movie['star'])      

#db.movies.update_one({'title' : '매트릭스'}, {'$set' : {'star' : 0} })