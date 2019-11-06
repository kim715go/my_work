#importing necessary libraries

import pandas as pd  #for excel exporting

#libraries for search result parsing
import requests
from bs4 import BeautifulSoup

import datetime

class searchMachine :
    def __init__(self):
        self.defaultURL = "https://dapi.kakao.com/v2/search/tip"
        self.headers = {'Content-Type': 'application/json; charset=utf-8',
                        'Authorization': 'KakaoAK ' #개인별 부여}
        self.oneResOutput = 50
        self.parameters = {'sort':'accuracy', 'page':1, 'size':self.oneResOutput, 'query':""} #size : the num of result for each page!

        self.takeSearchWord()

    def takeSearchWord(self):
        print("다음 팁 검색을 시작합니다...")
        self.parameters['query'] = str(input("검색어를 입력하세요 : "))
        self.adjustParameters()

    def getHTML(self, address):
        return BeautifulSoup(requests.get(address).text, 'html.parser')

    def getResultObject(self):
        return requests.get(self.defaultURL, headers = self.headers, params = self.parameters)

    def search(self, numOfRes):
        full = numOfRes // self.oneResOutput

        allItems = []
        self.totalNum = 0

        for i in range(1, full+2):
            self.parameters['page'] = i
            res = self.getResultObject()
            if res.status_code == 200 : 
                resJSON = res.json()
                if resJSON['meta']['is_end'] : 
                    self.totalNum = resJSON['meta']['pageable_count']
                    allItems += resJSON['documents'][:self.totalNum-50*(i-1)]
                    break
                else : 
                    allItems += resJSON['documents']
            else : 
                print("검색 오류가 발생했습니다. 수집을 종료합니다.")
                break

        try : 
            if self.totalNum :
                pass
            else : 
                self.totalNum = resJSON['meta']['pageable_count']  # get the whole number of the results

        except NameError:
            pass

        self.allItems = allItems

    def adjustParameters(self):
        print("검색 정보를 수집 중입니다...")
        self.search(1)
        print("약 %s개의 검색 결과를 수집할 수 있습니다." % self.totalNum)
        
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
                self.numOfResWanted = int(input("모든 검색 결과를 수집하시려면 0을 입력하시고, 수집 개수를 지정하시려면 2500이하의 자연수를 입력하세요 : "))
            except :
                print("잘못된 입력입니다. 다시 입력해 주세요.")
            else :
                if self.numOfResWanted == 0 :
                    self.numOfResWanted = self.totalNum
                    break
                elif 0 < self.numOfResWanted <= 2500 :
                    break
                else :
                    print("검색 결과 수는 1 이상 2500 이하이어야 합니다. 다시 입력해 주세요.")

        while True : #get sortWay
            sortInput = str(input("결과는 정확도 순으로 정렬됩니다. 이대로 진행할까요? (Y/N) "))
            if sortInput in ['y', 'Y'] :
                break
            elif sortInput in ['n', 'N'] :
                print("검색 결과는 최신순으로 정렬됩니다.")
                self.parameters['sort']= 'recency'
                break
            else :
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")

        while True:
            temp = str(input("지금까지 입력된 대로 검색을 진행할까요? (Y/N) "))

            if temp in ['y', 'Y']:
                self.mainSearch()
                break
            elif temp in ['n', 'N']:
                print("처음으로 되돌아 갑니다...")
                self.takeSearchWord()
                break
            else:
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")

    def mainSearch(self):
        self.search(self.numOfResWanted)
        self.makeDataFrame()

    def getItemInTag(self, bs4Object, tagName, *args, **kwargs):
        return bs4Object.find(tagName, *args, **kwargs).text.strip()

    def makeDataFrame(self):
        #dataGather = {'제목':[], '일시':[], '내용':[], '링크':[]}
        dataGather = {'제목':[], '날짜':[], 'ID':[], '질문내용':[], '링크':[]}
        numOfErrors = 0
        totalLength = len(self.allItems)

        for index, item in enumerate(self.allItems, 1) :
            link = item['q_url']
            dataGather['링크'].append(link)
            dataGather['제목'].append(BeautifulSoup(item['title'], 'lxml').text)
            dataGather['날짜'].append(item['datetime'][:10])

            #pubDate = item.pubdate.get_text(strip=True)
            #pubDate = datetime.datetime.strptime(pubDate,'%a, %d %b %Y %H:%M:%S %z')
            #pubDate = datetime.datetime.strftime(pubDate, '%Y-%m-%d %H:%M:%S')
            #dataGather['일시'].append(pubDate)
            #dataGather['내용'].append(BeautifulSoup(item.description.get_text(strip=True), 'lxml').get_text())

            bs4Item = self.getHTML(link)
            try :
                dataGather['ID'].append(self.getItemInTag(bs4Item, 'a', {'class':'link_user'}))
            except AttributeError:
                dataGather['ID'].append("")
                dataGather['질문내용'].append("열람 실패 - 필요한 경우 직접 확인")
                numOfErrors += 1
            else :
                dataGather['질문내용'].append(self.getItemInTag(bs4Item, 'div', {'class':'txt_collect'}))

            if index % 50 == 0 :
                print(index, '/', totalLength)

        self.resData = pd.DataFrame(dataGather)
        self.numOfErrors = numOfErrors
        self.fileWrite()

    def fileWrite(self):
        print("검색 수집이 완료되었습니다. 총 %d개의 검색 결과가 수집되었습니다." % self.resData.shape[0])
        fileName = "다음 팁 검색_" + self.parameters['query'] + "_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".xlsx"
        self.resData['연도'] = [x[:4] for x in self.resData['날짜']]
        self.resData = self.resData[['제목', '연도', '날짜', 'ID', '질문내용', '링크']]
        self.resData.to_excel(fileName, index=False)
        print(fileName + "에 결과가 저장되었습니다.")
        print("%d개의 웹페이지는 세부 내용을 수집하지 못하였습니다." % self.numOfErrors)
        temp = str(input("새 검색을 시작하시겠습니까? (Y/N) "))

        while True :
            if temp in ['y', 'Y']:
                self.takeSearchWord()
                break
            elif temp in ['n', 'N']:
                break
            else:
                print("잘못된 입력입니다. y 또는 n을 입력해 주세요. 대소문자는 구분하지 않습니다.")


if __name__ == "__main__" :
    sM = searchMachine()