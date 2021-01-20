from datetime import datetime

from django.shortcuts import render

# Create your views here.

def signup(request):
    # 오늘 날짜 : ex) Novermber 30
    todayIs = str(datetime.today().strftime("%B %d"))


    return render(request, 'signup.html', {'todayIs': todayIs})


def login(request):
    # 오늘 날짜 : ex) Novermber 30
    todayIs = str(datetime.today().strftime("%B %d"))


    return render(request, 'login.html', {'todayIs': todayIs})
