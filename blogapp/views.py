import logging
import time
import traceback

from django.shortcuts import render, redirect
import requests
import json
import asyncio
from urllib.request import Request, urlopen
import asyncio
from datetime import datetime

from stockWebProgramming2.oracleWork import bringmyStocks, isThere,insertInto_my_stock,delete_my_stock

sampleUrl = 'https://cloud.iexapis.com/stable/stock/aapl/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65'
sampleDate = []

#오늘 날짜 : ex) Novermber 30
todayIs = str(datetime.today().strftime("%B %d"))

# Create your views here.

# *** 메인화면(즐겨찾기한 주식 조회화면) ***
def goMainPage(request):

    starttime=time.time()

    # 즐겨찾기한 목록 조회
    # select stock_name from my_stock order by stock_name asc
    myStocks = bringmyStocks()

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

    print("#       #       #   #######   #         #####       #####       #         #   ###### ")
    print(' #     # #     #   #         #        #      #    #      #     ##      ##   # ')
    print('  #   #   #   #   #######   #        #           #       #    # #    # #   ######    ')
    print('   # #     # #   #         #         #      #    #      #    #   # #  #   #    ')
    print('    #	    #  #######   #######     #####       #####     #     #  #   ######  ')
    print('Loading Time:'+str(time.time()-starttime))

    return render(request, 'mainPage.html', {'stock_info': apiList,'todayIs':todayIs})


# *** 주식화면(주식 자세히 조회화면 ***)
def goStockPage(request):

    # apiListValue: 주식 정보들이 포함될 딕셔너리
    apiListValue = {}

    ## 예외처리
    # 1) except: 즐겨찾기 추가 버튼을 눌러 goStockPage를 호출한 경우 (메인페이지에서 눌러 symbol값을 들고오지 않아 api요청이 되지 않을 경우)
    # 2) 그외 : 메인페이지에서 symbol값을 들고와 정상적으로 api가 호출된 경우
    try:
        symbol = request.GET.get("symbol")
        api_request = requests.get(
            'https://cloud.iexapis.com/stable/stock/' + symbol + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')

    except:
        print('오류메시지')

        ## redirect할 symbol
        symbolR = request.GET.get("hiddenSymbol1")

        try:
            insertInto_my_stock(symbolR)
        except:
            delete_my_stock(symbolR)
        finally:
            # return redirect('goMainPage')
            return redirect('http://127.0.0.1:8000/stockpage?symbol='+symbolR)

    else:


        try:
            # AAPL / Apple Inc / 123.75$
            # apiListValue[symbol,companyName,종료주가,종료주가%,장외시간주가,장외주가%,open,low,high,시가총액,p/e,거래량]
            apiListValue["symbol"] = json.loads(api_request.content)["quote"]["symbol"]
            apiListValue["cmpName"] = json.loads(api_request.content)["quote"]["companyName"]
            apiListValue["peRate"] = json.loads(api_request.content)["quote"]["peRatio"]

            ## select COUNT(*) from my_stock where stock_name ='AAPL' 쿼리 값
            apiListValue["isThere"] = isThere(symbol)[0]

            # 시가총액
            mrkCap = (int(json.loads(api_request.content)["quote"]["marketCap"]))

            if mrkCap > 1000000000000:
                mrkCap = str(round(mrkCap / 1000000000000, 2)) + "T"
            elif mrkCap > 1000000000:
                mrkCap = str(round(mrkCap / 1000000000, 2)) + "B"
            elif mrkCap > 1000000:
                mrkCap = str(round(mrkCap / 1000000, 2)) + "M"
            apiListValue["mrkCap"] = mrkCap

            # 어제 대비 주가 변화율
            # changePercent=str(round((json.loads(api_request.content)["quote"]["changePercent"]*100), 2))+"%"
            # apiListValue["changePer"] =changePercent
            changePercent = (round((json.loads(api_request.content)["quote"]["changePercent"] * 100), 2))
            apiListValue["changePer"] = changePercent

            # 현재 주가 (최근 조회된 주가)
            latestPrice = str(round(json.loads(api_request.content)["quote"]["latestPrice"], 2)) + "$"
            apiListValue["latestPrice"] = latestPrice

            # 장외시간 주가(제대로 되는진 모르겠음)
            apiListValue["exPrice"] = str(json.loads(api_request.content)["quote"]["extendedPrice"]) + "$"
            apiListValue["extendedChangePercent"] = str(
                json.loads(api_request.content)["quote"]["extendedChangePercent"]) + "$"

            ## 추가 예정일 값들 : 거래량, 종료주가, 종료주가 퍼센트, open, low, high
            ## 추후 웹 크롤링 또는 정확한 값이 파악되면 추가될 예정

        except Exception as e:
            apiListValue = e

        print(apiListValue)
        return render(request, 'stockPage.html', {'stock_info': apiListValue, 'todayIs': todayIs})








# *** 즐겨찾기 주식 추가(주식 자세히 redirect)
def addMyStock(request):
    insertInto_my_stock()
    return redirect('goMainPage')


# *** 즐겨찾기 주식 삭제(주식 자세히 redirect)
def deleteMyStock(request):
    delete_my_stock()
    return redirect('goMainPage')
