from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.conf import settings


def homepage(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

def bok_board(request):
    if request.method == 'GET':
        return render(request, 'pages/board.html', {
            'kind_of_messages': 'bok'
        })
    elif request.method == 'POST':
        print('test')
    return HttpResponseBadRequest('Method not allowed')

def planet_board(request):
    if request.method == 'GET':
        return render(request, 'pages/board.html', {
            'kind_of_messages': 'planet'
        })
    elif request.method == 'POST':
        print('test')
    return HttpResponseBadRequest('Method not allowed')

def store_coordinates(request):
    if request.method == 'POST':
        return HttpResponse("ok")
    return HttpResponseBadRequest('Method not allowed')
