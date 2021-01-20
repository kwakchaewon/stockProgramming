from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.

def signup(request):
    # 오늘 날짜 : ex) Novermber 30
    todayIs = str(datetime.today().strftime("%B %d"))


    if request.method == "POST":
        if request.POST["userPwd1"] == request.POST["userPwd2"]:
            user = User.objects.create_user(
            username = request.POST["userId"], password=request.POST["userPwd1"])
            auth.login(request, user)


            ## 회원가입 성공 => 메인화면으로
            return redirect('http://127.0.0.1:8000/')

        ## 비밀번호 / 비밀번호 확인 다름 => signup로 되돌아감
        return render(request, 'signup.html', {'todayIs': todayIs})

    ## post 요청이 정상적으로 오지 않은 경우 => signup로 되돌아감
    return render(request, 'signup.html', {'todayIs': todayIs})


def login(request):
    # 오늘 날짜 : ex) Novermber 30
    todayIs = str(datetime.today().strftime("%B %d"))

    return render(request, 'login.html', {'todayIs': todayIs})
