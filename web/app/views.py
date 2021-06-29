from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache, caches
from django.conf import settings
from .models import Message, Location, Audio
from pydub import AudioSegment
from io import BytesIO
from django.core.files.base import File
import json
import uuid

CACHE_TTL = getattr(settings, 'CACHE_TTL', 3600)

@cache_page(CACHE_TTL)
def homepage(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def map_bok(request):
    if request.method == 'GET':
        return render(request, 'pages/map.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def martesana_page(request):
    if request.method == 'GET':
        return render(request, 'pages/martesana.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def eugenio_dog_life(request, message=None):
    if request.method == 'GET':
        open_modal = False
        if message:
            open_modal = True
        return render(request, 'pages/eugenio_dog_life.html', {
            'open_modal': open_modal
        })
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def donation(request):
    if request.method == 'GET':
        return render(request, 'pages/homepage.html', {})
    return HttpResponseBadRequest('Method not allowed')

@cache_page(CACHE_TTL)
def about_me(request):
    if request.method == 'GET':
        return render(request, 'pages/about_me.html', {})
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
        age = request.POST.get('age')

        if message and username and age:
            try:
                Message.objects.create(
                    text=message,
                    user=username,
                    age=age
                )
            except:
                return render(request, 'pages/board.html', {
                    'form_response': 'Ops.. Sembrerebbe che qualche campo sia mancante oppure non sia valido.',
                    'error': True
                })
            return render(request, 'pages/board.html', {
                'form_response': 'Il tuo messaggio è stato inviato, verrà revisionato il prima possibile, grazie!',
                'error': False
            })
        return render(request, 'pages/board.html', {
            'form_response': 'Ops.. Sembrerebbe che qualche campo sia mancante oppure non sia valido.',
            'error': True
        })

    return HttpResponseBadRequest('Method not allowed')

@csrf_exempt
def store_coordinates(request):
    if request.method == 'POST':
        bok_token = getattr(settings, 'BOK_GPS_TOKEN', None)
        body_decoded = request.body.decode('utf-8')
        print(body_decoded)
        body_splitted = body_decoded.split('&')
        print(body_splitted)
        for data in body_splitted:
            data_splitted = data.split('=')
            if data_splitted[0] == 'longitude':
                longitude = data_splitted[1]
            elif data_splitted[0] == 'latitude':
                latitude = data_splitted[1]
            elif data_splitted[0] == 'token':
                token = data_splitted[1]

        print(latitude)
        print(longitude)
        print(token)
        if bok_token == token and latitude and longitude:
            Location.objects.create(
                name='coordinate',
                slug=uuid.uuid4(),
                coordinate_x=latitude,
                coordinate_y=longitude
            )

            return HttpResponse('ok')
        return HttpResponseBadRequest('Something wrong happend or has been sent')
    return HttpResponseBadRequest('Method not allowed')

def get_coordinates(request):
    if request.method == 'GET':
        context_cache = caches['context-processor']
        locations_key = 'esiva.it/locations'
        roads_key = 'esiva.it/roads'
        live_points_key = 'esiva.it/live-point'

        locations = context_cache.get(locations_key, None)
        roads = context_cache.get(roads_key, None)
        live_points = context_cache.get(live_points_key, None)

        if locations is None or roads is None or live_points is None:
            roads_query = Location.objects.all().order_by('created_at')

            roads = []
            for point in roads_query:
                roads.append([point.coordinate_y, point.coordinate_x])

            if len(roads):
                live_points = roads[-1]
            else:
                live_points = []

            locations = list(roads_query.filter(is_city=True).values())

            context_cache.set(
                live_points_key, json.dumps(live_points, default=str), timeout=CACHE_TTL
            )
            context_cache.set(
                roads_key, json.dumps(roads, default=str), timeout=CACHE_TTL
            )
            context_cache.set(
                locations_key, json.dumps(locations, default=str), timeout=CACHE_TTL
            )
        else:
            live_points = json.loads(live_points)
            roads = json.loads(roads)
            locations = json.loads(locations)

        return JsonResponse({
            'live_points': live_points,
            'roads': roads,
            'locations': locations
        })
    return HttpResponseBadRequest('Method not allowed')

@login_required
def invalidate_cache(request):
    if request.method == 'GET':
        caches['default'].clear()
        caches['context-processor'].clear()
        return HttpResponse("ok")
    return HttpResponseBadRequest('Method not allowed')

def store_audio(request):
    if request.method == 'POST':
        audioFile = request.FILES.get('file', None)

        if audioFile:
            bytes_audio = BytesIO(audioFile.read())
            audio = AudioSegment.from_file(bytes_audio)
            wav = audio.export('people_file.wav', format='wav')

            with open('people_file.wav', 'rb') as file:
                Audio.objects.create(
                    file = File(file)
                )

            return JsonResponse({'openModal': True})
        return HttpResponseBadRequest('Somethings wrong happed with sending and retrieving the data')
    return HttpResponseBadRequest('Method not allowed')

def store_file_audio(request):
    if request.method == 'POST':
        file = request.FILES['audiofile']
        if file:
            Audio.objects.create(
                file = file
            )

            return redirect('eugenio-dog-life-sent', message='sent')
        return HttpResponseBadRequest('File not found')
    return HttpResponseBadRequest('Method not allowed')
