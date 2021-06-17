from django.conf import settings
from django.core.cache import caches
import json

from src.models import Location, Message

def process_context(request):

    cache = caches['context-processor']
    cache_timeout = 3600

    road_key = 'esiva.it/roads'
    road = cache.get(road_key, None)
    road = None
    if road is None:
        road_query = Location.objects.all().order_by('created_at')

        road = []
        for point in road_query:
            road.append([point.coordinate_y, point.coordinate_x])

        road = json.dumps(road)

        cache.set(road_key, road, timeout=cache_timeout)

    locations_key = 'esiva.it/locations'
    locations = cache.get(locations_key, None)
    if locations is None:
        try:
            locations = json.dumps(list(road_query.filter(is_city=True).values()), default=str)
        except:
            locations = json.dumps(list(Location.objects.filter(is_city=True).values()), default=str)

        cache.set(locations_key, locations, timeout=cache_timeout)

    bok_messages_key = 'esiva.it/bok-messages'
    planet_messages_key = 'esiva.it/planet-messages'
    bok_messages = cache.get(bok_messages_key, None)
    planet_messages = cache.get(planet_messages_key, None)
    if bok_messages is None or planet_messages:
        messages = Message.objects.filter(is_reviewed=True).order_by('created_at')

        bok_messages = list(messages.filter(kind_of='bok').values())
        planet_messages = list(messages.filter(kind_of='planet').values())

        cache.set(planet_messages_key, planet_messages, timeout=cache_timeout)
        cache.set(bok_messages_key, bok_messages, timeout=cache_timeout)

    return {
        'MAPBOX_TOKEN': settings.MAPBOX_TOKEN,
        'LOCATIONS': locations,
        'ROAD': road,
        'PLANET_MESSAGES': planet_messages,
        'BOK_MESSAGES': bok_messages
    }
