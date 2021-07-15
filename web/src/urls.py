"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app.views import (
    homepage,
    map_bok,
    martesana_page,
    thought_board,
    eugenio_dog_life,
    donation,
    about_me,
    partners,
    live_page,
    store_coordinates,
    get_coordinates,
    invalidate_cache,
    store_audio,
    store_file_audio
)

urlpatterns = [
    path('5301fs/', admin.site.urls),
    path('', homepage, name='homepage'),

    path('dove-sei-bok', map_bok, name='map-bok'),

    path('martesana-racconta', martesana_page, name='martesana-page'),

    path('bacheca-pensieri', thought_board, name='thought-board'),
    path('dai-vita-eugenio-cane/<str:message>', eugenio_dog_life, name='eugenio-dog-life-sent'),
    path('dai-vita-eugenio-cane', eugenio_dog_life, name='eugenio-dog-life'),

    path('donazioni', donation, name='donation'),
    path('about-me', about_me, name='about-me'),
    path('partners', partners, name='partners'),
    path('live', live_page, name='live'),

    # API urls
    path('api/store-coordinates', store_coordinates, name='store-coordinates'),
    path('api/get-coordinates', get_coordinates, name='get-coordinates'),
    path('api/invalidate-cache', invalidate_cache, name='invalidate-cache'),
    path('api/store-audio', store_audio, name='store-audio'),
    path('api/store-file-audio', store_file_audio, name='store-file-audio')
]
