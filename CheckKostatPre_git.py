
# coding: utf-8
# 통계청 최신 보도자료를 텔레그램으로 보내기
# filename : CheckKostatPre.py
# 개발언어 : Python 3
# 버전 :  1.0
# 작성일 : 2019. 9. 29.

import requests
from bs4 import BeautifulSoup
import urllib
import urllib3

urllib3.disable_warnings()
http = urllib3.PoolManager()

BOARD_URL = "http://kostat.go.kr/portal/korea/kor_nw/1/1/index.board"
DOMAIN = "https://kostat.go.kr/"
filename = 'LatestNoKostatPre.txt'

# telegram url(change your bot API token)
Teleg_URL = "https://api.telegram.org/bot230190712:AGHTKGdIVC134_8Gi1GYUsvHx87BlpOeyS3/sendMessage?chat_id=65796221&text="

# 2차원 배열(box) 선언과 초기화 ([0]번호, [1]제목, [2]URL)
box = [['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','','']]

# 파일에서 게시물 번호 가져오기
def GetTheNoFromFile():
    input_file = open(filename, 'r')
    fileNo = input_file.readline()
    input_file.close()
    return(fileNo)

# 최신 게시물번호를 파일에 덮어쓰기
def UpdateTheNewNo(strNewNo):
    output_file = open(filename, 'w')
    output_file.write(strNewNo)
    output_file.close()

# 텔레그램으로 알람 보내기
def SendTelegram(title, link):
    strTelMsg = '{}{}{}{}'.format(Teleg_URL, urllib.parse.quote("[통계청 보도자료]\n"), urllib.parse.quote(title), urllib.parse.quote(link))
    http.request('GET', strTelMsg).data
    
# 현재 최신 게시물번호 가져오기    
def GetTheLatestNo():
    
    # 1. 홈페이지에 GET 접속
    response = requests.get(BOARD_URL)
    
    # 2. BeautifulSoup을 이용하여 css selector를 이용할수 있는 html 객체 형태로 파싱
    dom = BeautifulSoup(response.content, "html.parser")
    
    # 3. 최신 게시물번호 구하기
    latestNum = dom.select_one(".num").text
    
    return(latestNum)

#------------------< Main 함수 >----------------#

# 파일에서 기존 게시물번호를 전역변수 NoFromFile에 저장
NoFromFile = GetTheNoFromFile()

# 현재 최신 게시물번호를 가져와서 전역변수 LatestNo에 저장
LatestNo = GetTheLatestNo()

if int(LatestNo) > int(NoFromFile):   
    
    num = int(LatestNo) - int(NoFromFile)
    
    # 최신 게시물번호를 파일에 쓰기
    # UpdateTheNewNo(LatestNo)

    # 1. 홈페이지에 GET 접속
    response = requests.get(BOARD_URL)
    
    # 2. BeautifulSoup을 이용하여 css selector를 이용할수 있는 html 객체 형태로 파싱
    dom = BeautifulSoup(response.content, "html.parser")
    
    # 3. 첫 페이지 게시물번호 10개 box에 저장하기

    # 3-1. 첫 페이지 10개 게시물 번호 구하기
    myNum = dom.select(".num")

    # 3-2. 첫 페이지 10개 게시물 제목과 URL 구하기   
    myList = dom.find_all('a', {'class':'title'})    

    # 3-3. box 리스트에 10개 게시물 정보(번호, 제목, URL) 집어넣기
    for i in range(0,10):
        box[i][0] = myNum[i].text               # 게시물 번호
        box[i][1] = myList[i].text              # 게시물 제목
        box[i][2] = DOMAIN + myList[i]['href']  # 게시물 URL
    
    # 텔레그램으로 최신 보도자료 정보 보내기
    for j in range(0, num):
        SendTelegram(box[j][1], box[j][2])
