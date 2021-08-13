from django.http import JsonResponse
from webapp import services as s
from django.core.cache import cache

def ping(requests):
    return JsonResponse({'data':'pong'})

def get(requests):
    nocache = requests.META['HTTP_NOCACHE']
    scode = requests.GET['scode']
    metar_data = s.services().getData(nocache, scode)
    return JsonResponse({'data': metar_data})