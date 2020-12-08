from django.shortcuts import render
import requests
import json


def stock(request):
    # requests.get함수를 이용해서 api주소에 요청을 보낸다.
    api_requests = requests.get(
        'https://cloud.iexapis.com/stable/stock/aapl/book?token=pk_cc9d0be588704852a3e1b6e3c91b1e65')

    try:
        # json 형식으로 반환된걸 그대로 읽어온후 api라는 변수에 저장
        api = json.loads(api_requests.content)
    except Exception as e:
        api = e

    print(api)
    return render(request, 'index2.html', {'stock_info': api})


def home(request):
    return render(request, 'index2.html', {})
