from django.shortcuts import render
import requests
import json
import callStockApi as CSA

# Create your views here.
def index(request):

    return render(request, 'index.html')


def index2(request):

    # 즐겨찾기한 목록 (예시 나중에는 오라클에서 가져올 예정)
    myStocks=['aapl','qcom','tsla','amzn','amd','ba','dal','fb','googl','intc','ko','lulu','ma','msft','nflx','nke','nvda','sbux','tsm','uber','v']

    # apiList : html로 보내질 리스트 / value값들로 구성됨
    apiList=[]






    # 즐겨찾기에 추가된 주식들을 각각 api로 주식정보들 가져오고 동적 리스트에 할당
    for i in range(0, len(myStocks)):

        # apiListValue: 각 종목의 주식 정보들이 포함될 딕셔너리
        apiListValue={}

        api_requests = requests.get(
            'https://cloud.iexapis.com/stable/stock/' + myStocks[i] + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
        try:
            # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
            # locals()['myStock' + str(i)] = json.loads(api_requests.content)
            apiListValue["symbol"]= json.loads(api_requests.content)["quote"]["symbol"]
            apiListValue["cmpName"] = json.loads(api_requests.content)["quote"]["companyName"]

        except Exception as e:
            apiListValue=e
        apiList.append(apiListValue)
    print(apiList)

    return render(request, 'index2.html',
                  {'stock_info': apiList})






    # # 애플 정보
    # api_requests = requests.get(
    #     'https://cloud.iexapis.com/stable/stock/'+'aapl'+'/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    # try:
    #     # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
    #     api1 = json.loads(api_requests.content)
    # except Exception as e:
    #     api1 = e
    #
    #
    # # 퀄컴 정보
    # api_requests = requests.get(
    #     'https://cloud.iexapis.com/stable/stock/' + 'qcom' + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    # try:
    #     # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
    #     api2 = json.loads(api_requests.content)
    # except Exception as e:
    #     api12 = e
    #
    #
    # # 테슬라
    # api_requests = requests.get(
    #     'https://cloud.iexapis.com/stable/stock/' + 'tsla' + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    # try:
    #     # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
    #     api3 = json.loads(api_requests.content)
    # except Exception as e:
    #     api3 = e
    #
    #
    # # 아마존
    # api_requests = requests.get(
    #     'https://cloud.iexapis.com/stable/stock/' + 'amzn' + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    # try:
    #     # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
    #     api4 = json.loads(api_requests.content)
    # except Exception as e:
    #     api4 = e
    #
    #
    # return render(request, 'index2.html', {'stock_info1': api1, 'stock_info2': api2, 'stock_info3': api3, 'stock_info4': api4})