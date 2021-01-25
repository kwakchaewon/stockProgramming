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


    ## 로그인 4가지 경우의 수
    ##  1_ userId 쿠키가 존재하며 정상적으로 로그인 되는 경우 => 메인화면으로
    ##  2_ userId 쿠키는 존재하나 로그인은 되지 않는 경우(아이디나 비밀번호가 틀린 경우) => 로그인 화면으로
    ##  3_ 로그인 쿠키가 존재하지 않아 요청받아 로그인이 된 경우 => 쿠키에 저장 후 메인 화면으로
    ##  4_ 로그인 쿠키가 존재하지 않아 요청받아 로그인을 시도했으나 틀린 경우 => 로그인 창으로


    # 쿠키 userId 값이 있다면 user로그인 시도
    if request.COOKIES.get('userId') is not None:
        userId = request.COOKIES.get('userId')
        passwrd = request.COOKIES.get('passwrd')
        user = auth.authenticate(request, username=userId, password=passwrd)


        ##  1_ userId 쿠키가 존재하며 정상적으로 로그인 되는 경우 => 메인화면으로
        if user is not None:
            auth.login(request, user)
            return redirect('http://127.0.0.1:8000/')


        ##  2_ userId 쿠키는 존재하나 로그인은 되지 않는 경우(아이디나 비밀번호가 틀린 경우) => 로그인 화면으로
        ## 한번 바꿔야할듯 -> 오는 경우가 이미 쿠키에 로그인값들이 전달된 상태에서 다시 로그인창에서 로그인 시도 할 경우 이 쪽으로 오더라
        else:
            return render(request, 'login.html', {'todayIs': todayIs, 'error': 'ID or password is incorrect'} )



    #쿠키가 없는 경우
    elif request.method == "POST":
        userId = request.POST['userId']
        passwrd = request.POST['userPwd']
        user = auth.authenticate(request, username=userId, password=passwrd)


        ##  3_ 로그인 쿠키가 존재하지 않아 요청받아 로그인이 된 경우 => 쿠키에 저장 후 메인 화면으로
        if user is not None:
            auth.login(request, user)


            # if request.POST.get("keep_login") == "TRUE":
            #     response = redirect('http://127.0.0.1:8000/')
            #     response.set_cookie('userId', userId)
            #     response.set_cookie('userPwd', passwrd)
            #     return response

            response = redirect('http://127.0.0.1:8000/')
            response.set_cookie('userId', userId)
            response.set_cookie('userPwd', passwrd)
            return response


            # return redirect('http://127.0.0.1:8000/')

        ##  4_ 로그인 쿠키가 존재하지 않아 요청받아 로그인을 시도했으나 틀린 경우 => 로그인 창으로
        else:
            return (request, 'login.html', {'todayIs': todayIs , 'error': 'ID or password is incorrect'} )



    ## 그밖에
    else:
        return render(request, 'login.html', {'todayIs': todayIs})

    return render(request, 'login.html', {'todayIs': todayIs})



def logout(request):
    response = redirect('http://127.0.0.1:8000/')
    response.delete_cookie('userId')
    response.delete_cookie('userPwd')
    auth.logout(request)
    return response