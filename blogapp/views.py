from django.shortcuts import render
import requests
import json
import callStockApi as CSA

# Create your views here.
def index(request):

    return render(request, 'index.html')


def index2(request):

    # 즐겨찾기한 목록
   myStocks=['aapl' ,'qcom' ,'tsla' ,'amzn' ]

    for mystock in myStocks:
        locals()[myStock]=


    # 애플 정보
    api_requests = requests.get(
        'https://cloud.iexapis.com/stable/stock/'+'aapl'+'/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    try:
        # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
        api1 = json.loads(api_requests.content)
    except Exception as e:
        api1 = e


    # 퀄컴 정보
    api_requests = requests.get(
        'https://cloud.iexapis.com/stable/stock/' + 'qcom' + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    try:
        # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
        api2 = json.loads(api_requests.content)
    except Exception as e:
        api12 = e


    # 테슬라
    api_requests = requests.get(
        'https://cloud.iexapis.com/stable/stock/' + 'tsla' + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    try:
        # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
        api3 = json.loads(api_requests.content)
    except Exception as e:
        api3 = e


    # 아마존
    api_requests = requests.get(
        'https://cloud.iexapis.com/stable/stock/' + 'amzn' + '/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')
    try:
        # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
        api4 = json.loads(api_requests.content)
    except Exception as e:
        api4 = e


    return render(request, 'index2.html', {'stock_info1': api1, 'stock_info2': api2, 'stock_info3': api3, 'stock_info4': api4})