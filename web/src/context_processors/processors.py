from django.conf import settings
from django.core.cache import caches
import json

from app.models import Location, Message

def process_context(request):

    cache = caches['context-processor']
    cache_timeout = getattr(settings, 'CACHE_TTL', 3600)

    road_key = 'esiva.it/roads'
    live_point_key = 'esiva.it/live-point'
    live_point = cache.get(live_point_key, None)
    road = cache.get(road_key, None)
    road = None
    if road is None or live_point is None:
        road_query = Location.objects.all().order_by('-created_at')

        road = []
        for point in road_query:
            road.append([point.coordinate_y, point.coordinate_x])

        if len(road):
            live_point = road[-1]
        else:
            live_point = []

        live_point = json.dumps(live_point)
        road = json.dumps(road)

        cache.set(live_point_key, live_point, timeout=cache_timeout)
        cache.set(road_key, road, timeout=cache_timeout)

    locations_key = 'esiva.it/locations'
    locations = cache.get(locations_key, None)
    if locations is None:
        try:
            locations = road_query.filter(is_city=True).values()
        except:
            locations = Location.objects.filter(is_city=True).values()

        locations = json.dumps(list(locations), default=str)

        cache.set(locations_key, locations, timeout=cache_timeout)

    thought_messages_key = 'esiva.it/thought-messages'
    thought_messages = cache.get(thought_messages_key, None)
    if thought_messages is None:
        thought_messages = list(Message.objects.filter(is_reviewed=True).order_by('created_at').values())

        cache.set(thought_messages_key, thought_messages, timeout=cache_timeout)

    return {
        'MAPBOX_TOKEN': settings.MAPBOX_TOKEN,
        'LIVE_POINT': live_point,
        'LOCATIONS': locations,
        'ROAD': road,
        'THOUGHT_MESSAGES': thought_messages,
    }
