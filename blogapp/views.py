import time

from django.shortcuts import render
import requests
import json
import asyncio
from urllib.request import Request, urlopen
import asyncio

sampleUrl = 'https://cloud.iexapis.com/stable/stock/aapl/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65'
sampleDate = []


# Create your views here.
def goMainPage(request):

    # *** 메인화면(즐겨찾기한 주식 조회화면) ***

    starttime=time.time()

    # 즐겨찾기한 목록 (예시 나중에는 오라클에서 가져올 예정)
    myStocks = ['aapl', 'qcom', 'tsla', 'amzn', 'amd', 'ba', 'dal', 'fb', 'googl', 'intc', 'ko', 'lulu', 'ma', 'msft',
                'nflx', 'nke', 'nvda', 'sbux', 'tsm', 'uber', 'v']

    # apiList : html로 보내질 리스트 / value값들로 구성됨
    apiList = []

    # urls : myStocks의 url들
    urls=[]

    for i in myStocks:
        urls.append('https://cloud.iexapis.com/stable/stock/' +
                    i + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')



    ####
    #
    # 비동기 함수_1: 기존의 방식대로 웹페이지에 값을 요청하면 로딩시간이 길어져 비동기 방식으로 변경
    # urlopen / read 함수 같이 웹페이지의 결과를 가져오는 함수는 결과가 나올 때까지 코드실행이 중단되고 로딩시간이 길어진다.
    # 이 때 네이티브 코루틴(파이썬 비동기) 안에서 i/o 함수를 실행하면 i/o 함수는 메인쓰레드를 중단시키지 않는다.
    # await loop.run_in_executor( None, 실행할 함수, 인수1, 인수2, ...) : loop 쓰레드에서 비동기로 함수 결과를 가져온다.
    #
    ####

    async def fetch(url):
        # apiListValue: 각 종목의 주식 정보들이 포함될 딕셔너리
        apiListValue = {}

        requestUrl = Request(url, headers= {'User-Agent': 'Mozilla/5.0'})
        response = await loop.run_in_executor(None, urlopen, requestUrl)
        
        # 비동기로 요청한 웹페이지를 바이트형식으로 담고 json형식으로 변경
        byteBuffer = await loop.run_in_executor(None, response.read)
        jsonValues= json.loads(byteBuffer.decode("utf-8"))

        apiListValue["symbol"] = jsonValues["quote"]["symbol"]
        apiListValue["cmpName"] = jsonValues["quote"]["companyName"]
        apiListValue["latestPrice"] = str(jsonValues["quote"]["latestPrice"]) + "$"
        apiList.append(apiListValue)
        return len(byteBuffer)

    ####
    #
    # 비동기함수_2:
    # 1. main에서는 네이티브 코루틴을 여러개 사용하는데 먼저 asyncio.ensure_future() 함수를 사용해 asyncio.Task객체를 생성하고 리스트로 만든다.
    #    태스크객체 = asyncio.ensure_future(코루틴객체 or 퓨처객체)
    #
    # 2. asyncio.gather는 모든 코루틴 객체가 끝날 때까지 기다린 뒤 결과를 반환한다.
    #    변수= await asyncio.gather (코루틴객체1, 코루틴객체2)
    #
    ####

    async def main():
        futures = [asyncio.ensure_future(fetch(url)) for url in urls]
        result = await asyncio.gather(*futures)


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()

    print('로딩시간:'+str(time.time()-starttime))
    return render(request, 'mainPage.html', {'stock_info': apiList})
