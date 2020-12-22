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
def index(request):
    # 즐겨찾기한 목록 (예시 나중에는 오라클에서 가져올 예정)
    myStocks = ['aapl', 'qcom', 'tsla', 'amzn', 'amd', 'ba', 'dal', 'fb', 'googl', 'intc', 'ko', 'lulu', 'ma', 'msft',
                'nflx', 'nke', 'nvda', 'sbux', 'tsm', 'uber', 'v']

    # apiList : html로 보내질 리스트 / value값들로 구성됨
    apiList = []

    # 즐겨찾기에 추가된 주식들을 각각 api로 주식정보들 가져오고 동적 리스트에 할당
    for i in range(0, len(myStocks)):

        # apiListValue: 각 종목의 주식 정보들이 포함될 딕셔너리
        apiListValue = {}

        api_requests = requests.get(
            'https://cloud.iexapis.com/stable/stock/' + myStocks[i] + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
        try:
            # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장

            # AAPL / Apple Inc / 123.75$
            apiListValue["symbol"] = json.loads(api_requests.content)["quote"]["symbol"]
            apiListValue["cmpName"] = json.loads(api_requests.content)["quote"]["companyName"]
            apiListValue["latestPrice"] = str(json.loads(api_requests.content)["quote"]["latestPrice"]) + "$"

        except Exception as e:
            apiListValue = e
        apiList.append(apiListValue)

    return render(request, 'index.html', {'stock_info': apiList})


def index2(request):
    starttime=time.time()

    # 즐겨찾기한 목록 (예시 나중에는 오라클에서 가져올 예정)
    myStocks = ['aapl', 'qcom', 'tsla', 'amzn', 'amd', 'ba', 'dal', 'fb', 'googl', 'intc', 'ko', 'lulu', 'ma', 'msft',
                'nflx', 'nke', 'nvda', 'sbux', 'tsm', 'uber', 'v']

    # apiList : html로 보내질 리스트 / value값들로 구성됨
    apiList = []


    # 즐겨찾기에 추가된 주식들을 각각 api로 주식정보들 가져오고 동적 리스트에 할당
    for i in range(0, len(myStocks)):

        async def getAsyncStock():
            # apiListValue: 각 종목의 주식 정보들이 포함될 딕셔너리
            apiListValue = {}
            api_requests = requests.get(
                'https://cloud.iexapis.com/stable/stock/' + myStocks[
                    i] + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
            try:
                # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
                # locals()['myStock' + str(i)] = json.loads(api_requests.content)
                apiListValue["symbol"] = json.loads(api_requests.content)["quote"]["symbol"]
                apiListValue["cmpName"] = json.loads(api_requests.content)["quote"]["companyName"]

            except Exception as e:
                apiListValue = e
            apiList.append(apiListValue)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(getAsyncStock())
        loop.close()

    loadingtime=time.time()-starttime
    print(loadingtime)
    return render(request, 'index2.html',
                  {'stock_info': apiList})



    # 비동기작업 해보기
def index3(request):
    starttime=time.time()
    myStocks = ['aapl', 'qcom', 'tsla', 'amzn', 'amd', 'ba', 'dal', 'fb', 'googl', 'intc', 'ko', 'lulu', 'ma', 'msft',
                'nflx', 'nke', 'nvda', 'sbux', 'tsm', 'uber', 'v']

    # apiList : html로 보내질 리스트 / value값들로 구성됨
    apiList = []

    urls=[]

    #비동기로 웹페이지 가져오기
    for i in myStocks:
        urls.append('https://cloud.iexapis.com/stable/stock/' +
                    i + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')

    async def fetch(url):
        # apiListValue: 각 종목의 주식 정보들이 포함될 딕셔너리
        apiListValue = {}

        request2 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = await loop.run_in_executor(None, urlopen, request2)
        page = await loop.run_in_executor(None, response.read)

        stringPage=page.decode("utf-8")
        jsonPage=json.loads(stringPage)

        apiListValue["symbol"] = jsonPage["quote"]["symbol"]
        apiListValue["cmpName"] = jsonPage["quote"]["companyName"]
        apiListValue["latestPrice"] = str(jsonPage["quote"]["latestPrice"]) + "$"
        apiList.append(apiListValue)
        return len(page)

    async def main():
        futures = [asyncio.ensure_future(fetch(url)) for url in urls]
        result = await asyncio.gather(*futures)


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()

    print('로딩시간:'+str(time.time()-starttime))
    return render(request, 'index.html', {'stock_info': apiList})
