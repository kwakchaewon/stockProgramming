"""stockWebProgramming2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import blogapp.views
import accounts.views

# path('/뒤에 나올 주소',실행될 함수이름,html에서 적용될 이름)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blogapp.views.goMainPage, name='mainPage'),
    path('stockpage', blogapp.views.goStockPage, name='stockPage'),
    path('signup',accounts.views.signup,name='signup'),
    path('login',accounts.views.login,name='login'),
]
