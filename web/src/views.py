from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from .models import Message

CACHE_TTL = getattr(settings, 'CACHE_TTL', 3600)

@cache_page(CACHE_TTL)
def homepage(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def bok_board(request):
    if request.method == 'GET':
        return render(request, 'pages/board.html', {
            'kind_of_messages': 'bok'
        })
    elif request.method == 'POST':
        message = request.POST.get('messageInput')
        username = request.POST.get('username')
        email = request.POST.get('email')

        if message and username and email:
            Message.objects.create(
                text=message,
                kind_of='bok',
                user=username,
                email=email
            )
            return render(request, 'pages/board.html', {
                'kind_of_messages': 'bok',
                'message': 'Message sent'
            })
        return HttpResponseBadRequest('One or more fields are missing or aren\'t allowed')
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def planet_board(request):
    if request.method == 'GET':
        return render(request, 'pages/board.html', {
            'kind_of_messages': 'planet'
        })
    elif request.method == 'POST':
        message = request.POST.get('messageInput')
        username = request.POST.get('username')
        email = request.POST.get('email')
        board = request.POST.get('board')

        if message and username and email:
            Message.objects.create(
                text=message,
                kind_of='planet',
                user=username,
                email=email
            )
            return render(request, 'pages/board.html', {
                'kind_of_messages': 'planet',
                'message': 'Message sent'
            })
        return HttpResponseBadRequest('One or more fields are missing or aren\'t allowed')

    return HttpResponseBadRequest('Method not allowed')

def store_coordinates(request):
    if request.method == 'POST':
        return HttpResponse("ok")
    return HttpResponseBadRequest('Method not allowed')

@login_required
def invalidate_cache(request):
    if request.method == 'GET':
        cache.clear()
        return HttpResponse("ok")
    return HttpResponseBadRequest('Method not allowed')
