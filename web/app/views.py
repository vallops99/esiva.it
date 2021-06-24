from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from .models import Message, Location
import json
import uuid

CACHE_TTL = getattr(settings, 'CACHE_TTL', 3600)

@cache_page(CACHE_TTL)
def homepage(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def map(request):
    if request.method == 'GET':
        return render(request, 'pages/map.html', {
            'only_bok': False
        })
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def map_bok(request):
    if request.method == 'GET':
        return render(request, 'pages/map.html', {
            'only_bok': True
        })
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def martesana_page(request):
    if request.method == 'GET':
        return render(request, 'pages/martesana.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def eugenio_dog_life(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def donation(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def about_me(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def partners(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def thought_board(request):
    if request.method == 'GET':
        return render(request, 'pages/board.html', {})
    elif request.method == 'POST':
        message = request.POST.get('messageInput')
        username = request.POST.get('username')
        email = request.POST.get('email')
        board = request.POST.get('board')

        if message and username and email:
            Message.objects.create(
                text=message,
                user=username,
                email=email
            )
            return render(request, 'pages/board.html', {
                'form_response': 'Message sent'
            })
        return HttpResponseBadRequest('One or more fields are missing or aren\'t allowed')

    return HttpResponseBadRequest('Method not allowed')

def store_coordinates(request):
    if request.method == 'POST':
        body = json.parse(request.body)
        if body and 'content' in body:
            content = body['content']
            if 'latitude' in content and 'longitude' in content:
                latitude = content['latitude']
                longitude = content['longitude']
                Location.objects.create(
                    name='coordinate',
                    slug=uuid.uuid4(),
                    coordinate_x=latitude,
                    coordinate_y=longitude
                )

                return HttpResponse("ok")
        return HttpResponseBadRequest('Something wrong happend or has been sent')
    return HttpResponseBadRequest('Method not allowed')

@login_required
def invalidate_cache(request):
    if request.method == 'GET':
        cache.clear()
        return HttpResponse("ok")
    return HttpResponseBadRequest('Method not allowed')
