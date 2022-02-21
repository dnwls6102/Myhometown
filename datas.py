from urllib.request import *
from bs4 import BeautifulSoup
import re, random

citylist = [
    "서울" ,"부산" ,'인천' , '광주', '세종', '대구', '대전', '울산',
    '경기 수원', '경기 고양', '경기 용인', '경기 성남', '경기 부천', '경기 화성',
    '경기 안산', '경기 남양주', '경기 안양', '경기 평택', '경기 시흥', '경기 파주',
    '경기 의정부', '경기 김포', '경기 광주', '경기 광명', '경기 군포', '경기 하남',
    '경기 오산', '경기 양주', '경기 이천', '경기 구리', '경기 안성', '경기 포천', '경기 의왕',
    '경기 양평', '경기 여주', '경기 동두천', '경기 가평', '경기 과천', '경기 연천',
    '강원 춘천', '강원 원주', '강원 강릉', '강원 동해', '강원 태백', '강원 속초', '강원 삼척',
    '강원 홍천', '강원 횡성', '강원 영월', '강원 평창', '강원 정선', '강원 철원', '강원 화천',
    '강원 양구', '강원 인제', '강원 고성', '강원 양양', '충북 청주', '충북 충주', '충북 제천',
    '충북 보은', '충북 옥천', '충북 영동', '충북 증평', '충북 진천', '충북 괴산', '충북 음성',
    '충북 단양', '충남 천안', '충남 공주', '충남 보령', '충남 아산', '충남 서산', '충남 논산',
    '충남 계룡', '충남 당진', '충남 금산', '충남 부여', '충남 서천', '충남 청양', '충남 홍성',
    '충남 예산', '충남 태안', '전북 전주', '전북 군산', '전북 익산', '전북 정읍', '전북 남원',
    '전북 김제', '전북 완주', '전북 진안', '전북 무주', '전북 장수', '전북 임실', '전북 순창',
    '전북 고창', '전북 부안', '전남 목포', '전남 여수', '전남 순천', '전남 나주', '전남 광양',
    '전남 담양', '전남 곡성', '전남 구례', '전남 고흥', '전남 보성', '전남 화순', '전남 장흥',
    '전남 강진', '전남 해남', '전남 영암', '전남 무안', '전남 함평', '전남 영광', '전남 장성',
    '전남 완도', '전남 진도', '전남 신안', '경북 포항', '경북 경주', '경북 김천', '경북 안동',
    '경북 구미', '경북 영주', '경북 영천', '경북 상주', '경북 문경', '경북 경산', '경북 군위',
    '경북 의성', '경북 청송', '경북 영양', '경북 영덕', '경북 청도', '경북 고령', '경북 성주',
    '경북 칠곡', '경북 예천', '경북 봉화', '경북 울진', '경북 울릉', '경남 창원', '경남 진주',
    '경남 통영', '경남 사천', '경남 김해', '경남 밀양', '경남 거제', '경남 양산', '경남 의령',
    '경남 함안', '경남 창녕', '경남 고성', '경남 남해', '경남 하동', '경남 산청', '경남 함양',
    '경남 거창', '경남 합천', '제주'
    ] #대한민국 행정구역 목록

stopwords = ['KBS', '리포터', '총국'] #불용어 목록
checked = [] #텍스트 중복확인 방지용 빈 리스트

count = {} #횟수 저장용 전역변수
#작동잘됨
#2009~2020 (2015, 2018 제외) 알고리즘
for i in [2009,2010,2011,2012,2013,2014,2016,2017,2019,2020]:
    page = urlopen('https://ko.wikipedia.org/wiki/6%EC%8B%9C_%EB%82%B4%EA%B3%A0%ED%96%A5%EC%9D%98_%EC%97%90%ED%94%BC%EC%86%8C%EB%93%9C_%EB%AA%A9%EB%A1%9D_({}%EB%85%84)'.format(i)) #마지막20XX%EB%85%84부분에서 년도만 바꿔주면 페이지 바뀜
    sp = BeautifulSoup(page, 'html.parser')
    pre = sp.find('pre')
    all_text = pre.get_text()
    episode_list = all_text.split('/')
    for episode in episode_list:
        for city in citylist:
            if city in episode:
                if city not in count:
                    count[city] = 1
                else:
                    count[city] +=1
#for i in count:
#    print("",i,":",count[i],"회")

#2015, 2018, 2021년 한정 알고리즘 (table을 통해 회차 구현)
for i in [2015, 2018, 2021]:
    wp = urlopen('https://ko.wikipedia.org/wiki/6%EC%8B%9C_%EB%82%B4%EA%B3%A0%ED%96%A5%EC%9D%98_%EC%97%90%ED%94%BC%EC%86%8C%EB%93%9C_%EB%AA%A9%EB%A1%9D_({}%EB%85%84)'.format(i)) #페이지 여는 명령
    soup = BeautifulSoup(wp, 'html.parser') #BeautifulSoup4 모듈 불러오기
    divlist= soup.find_all('div', {'class' : 'mw-parser-output'}) #class가 mw-collapsible-content인 div 속성 텍스트 찾기 (실제 자료형은 텍스트 상태가 아님)
    for div in divlist:
        tdlist = div.find_all('td') #mw-collapsible-content(방영목록 적힌 div)에서 td만 모아둔 것
        for td in tdlist:
            """ #1번 알고리즘 : 정규표현식을 이용한 횟수세기
            if re.match(r'.*\((\w{2}\s\w{2})\).*', td.get_text())
                #for city in citylist :
                    #if city in td.get_text():
                #print(re.search(r'.*\((\w{2}.*\w{2})\)', td.get_text()).group(1))
                if re.search(r'.*\((\w{2}.*\w{2})\).*', td.get_text()).group(1) not in dic:
                    dic[re.search(r'.*\((\w{2}.*\w{2})\).*', td.get_text()).group(1)] = 1
                else:
                    dic[re.search(r'.*\((\w{2}.*\w{2})\).*', td.get_text()).group(1)] += 1
                    """ #문제 : 이상한 데이터가 섞임(예: 최형진 셰프, 이후 미정 등) + 괄호 밖에 지역명이 써진 경우 세지를 못함
            for city in citylist: #2번 알고리즘 : 단순한 포함관계 이용한 횟수세기
                if city in td.get_text(): #2-1 : 중복 확인 안하고 그냥 세기 문제 : 중복으로 셈 (예: 경남 밀양 - 000리포터(부산총국)의 경우 경남 밀양 +1, 부산 +1), 쓸데없는 것을 셈 (예: 네트워크 1 - 미정(부산))
                #if city in td.get_text() and td.get_text() not in checked: #2-2 중복 확인 하고 세기 문제 : 쓸데없는 것을 셈 + 세야 할 것을 안세던가, 에피소드 명이 같을 경우 횟수에 추가하지 못함
                    if city not in count:
                        count[city] = 1
                        #checked.append(td.get_text())
                    else :
                        count[city] += 1
                        #checked.append(td.get_text())
#크롤링 정상적으로 되는지 확인
"""   
for i in count:
    print("",i,":",count[i],"회")
"""
def pickone():
    return random.sample(list(count.keys()), 2)
