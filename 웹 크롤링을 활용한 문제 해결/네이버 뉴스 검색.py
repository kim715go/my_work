#importing necessary libraries

from pandas import DataFrame as pdDF #for excel exporting

#libraries for search result parsing
from urllib.request import Request as uRequest
from urllib.request import urlopen as uUrlopen

from urllib.parse import quote_plus as uQuote_plus

import urllib.parse
from bs4 import BeautifulSoup

from datetime import datetime as dt

class searchMachine :
    def __init__(self):
        self.searchWord =""
        self.sortWay = 'sim'
        self.defaultURL = 'https://openapi.naver.com/v1/search/news.xml?'
        self.oneResOutput = 100

        self.headers = {
            'Host': 'openapi.naver.com',
            'User-Agent': 'curl/7.49.1',
            'Accept': '*/*',
            'Content-Type': 'application/xml',
            'X-Naver-Client-Id': "" #개인별 부여
            'X-Naver-Client-Secret': "" #개인별 부여
        }

        self.takeSearchWord()

    def takeSearchWord(self):
        print("네이버 뉴스 검색을 시작합니다...")
        self.searchWord = str(input("검색어를 입력하세요 : "))
        self.takeOtherInput()


    def _search_(self, startNum, displayNum):
        sortWay = 'sort=' + self.sortWay
        start = '&start=' + str(startNum)
        display = '&display=' + str(displayNum)
        query = '&query=' + uQuote_plus(self.searchWord)  # 사용자에게 검색어를 입력받아 quote_plus 함수로 UTF-8 타입에 맞도록 변환시켜 줍니다.
        fullURL = self.defaultURL + sortWay + start + display + query

        # HTTP 요청을 하기 전에 헤더 정보를 이용해 request 객체를 생성합니다. urllib 모듈에서 헤더 정보를 서버에 전달할 때 사용하는 대표적인 방법입니다.
        req = uRequest(fullURL, headers=self.headers)
        # 생성된 request객체를 uplopen함수의 인수로 전달합니다. 이렇게 되면 헤더 정보를 포함하여 서버에게 HTTP 요청을 하게 됩니다.

        f = uUrlopen(req)
        resultXML = f.read()
        xmlsoup = BeautifulSoup(resultXML, 'lxml')

        return xmlsoup

    def search(self, numOfRes):
        full = numOfRes // self.oneResOutput
        remains = numOfRes % self.oneResOutput

        allItems = []
        self.totalNum = 0

        for i in range(full):
            stN = i * self.oneResOutput + 1
            xmlsoup = self._search_(stN, self.oneResOutput)
            items = xmlsoup.find_all('item')
            allItems += items

        if remains:
            stN = full*self.oneResOutput + 1
            if stN > 1000 :
                redundunt = stN - 1000
                xmlsoup = self._search_(1000, remains+1)
                items = xmlsoup.find_all('item')
                items = items[redundunt:]
            else :
                xmlsoup = self._search_(stN, remains)
                items = xmlsoup.find_all('item')

            allItems += items
            self.totalNum = xmlsoup.total.string  # get the whole number of the results

        else:
            self.totalNum = xmlsoup.total.string  # get the whole number of the results

        self.allItems = allItems

    def takeOtherInput(self):
        print("검색 정보를 수집 중입니다...")
        self.search(1)
        print("총 %s개의 결과가 검색되었습니다. " % self.totalNum)
        print("이 중 상위 1099개까지의 검색 결과를 가져올 수 있습니다.")

        while True :
            temp = str(input("검색을 계속 할까요? (Y/N) "))

            if temp in ['y', 'Y']:
                break
            elif temp in ['n', 'N']:
                self.takeSearchWord()
                break
            else:
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")


        while True : #get numOfResWanted
            try :
                self.numOfResWanted = int(input("몇 개의 검색 결과를 가져오시겠습니까? 자연수로 입력해 주세요 : "))
            except :
                print("잘못된 입력입니다. 다시 입력해 주세요.")
            else :
                if 0 < self.numOfResWanted < 1100 :
                    break
                else :
                    print("검색 결과 수는 1 이상 1099 이하이어야 합니다. 다시 입력해 주세요.")

        while True : #get sortWay
            sortInput = str(input("결과는 정확도 순으로 정렬됩니다. 이대로 진행할까요? (Y/N) "))
            if sortInput in ['y', 'Y'] :
                break
            elif sortInput in ['n', 'N'] :
                self.sortWay = 'date'
                break
            else :
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")

        while True:
            temp = str(input("지금까지 입력된 대로 검색을 진행할까요? (Y/N) "))

            if temp in ['y', 'Y']:
                self.mainSearch()
                break
            elif temp in ['n', 'N']:
                self.takeOtherInput()
                break
            else:
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")

    def mainSearch(self):
        self.search(self.numOfResWanted)
        self.makeDataFrame()

    def makeDataFrame(self):
        dataGather = {'제목':[], '일시':[], '내용':[], '링크':[]}
        for item in self.allItems :
            dataGather['제목'].append(BeautifulSoup(item.title.get_text(strip=True), 'lxml').get_text())
            pubDate = item.pubdate.get_text(strip=True)
            pubDate = dt.strptime(pubDate,'%a, %d %b %Y %H:%M:%S %z')
            pubDate = dt.strftime(pubDate, '%Y-%m-%d %H:%M:%S')
            dataGather['일시'].append(pubDate)
            dataGather['내용'].append(BeautifulSoup(item.description.get_text(strip=True), 'lxml').get_text())
            dataGather['링크'].append(item.originallink.get_text(strip=True))

        self.resData = pdDF(dataGather)
        self.resData.index += 1
        self.fileWrite()

    def fileWrite(self):
        print("검색 수집이 완료되었습니다.")
        fileName = "네이버 뉴스 검색_" + self.searchWord + "_" + dt.now().strftime('%Y%m%d_%H%M%S') + ".xlsx"
        self.resData = self.resData[['제목', '일시', '내용', '링크']]
        self.resData.to_excel(fileName)
        print(fileName + "에 결과가 저장되었습니다.")
        temp = str(input("새 검색을 시작하시겠습니까? (Y/N) "))

        while True :
            if temp in ['y', 'Y']:
                self.takeSearchWord()
                break
            elif temp in ['n', 'N']:
                print('프로그램을 종료합니다...')
                exit()
            else:
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")


if __name__ == "__main__" :
    print('네이버 뉴스 검색 수집기 ver. 1.1\n배포일자 : 2018/07/20')
    sM = searchMachine()