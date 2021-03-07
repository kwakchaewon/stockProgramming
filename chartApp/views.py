from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.shortcuts import render

# Create your views here.


class ResultApiView(ApiView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = request.session.get('result')
        return Response(data)

    def result_detail(request):
        context = {}
        return render('chart.html', context)