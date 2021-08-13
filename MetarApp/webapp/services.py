import requests
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache

CACHE_TTL = getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)

class services(object):
    def getData(self,nocache,scode):
        if (nocache != "1" and cache.get(scode)):
            return cache.get(scode)
        metar_data = requests.get("https://tgftp.nws.noaa.gov/data/observations/metar/stations/"+scode+".TXT",).text
        metar_data = metar_data.split(sep=" ")
        time_and_station = metar_data[1].split(sep="\n")
        temperature = [i for i in metar_data if i.__contains__("/")]
        temperature_in_celsius = temperature[1].split("/")[0]
        temperature_in_farhenheit = round(int(temperature_in_celsius) * (9 / 5.0) + 32, 2)
        wind = metar_data[4]
        wind_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW",
                           "NNW", "W"]
        wind_direction = wind_directions[int((int(wind[0:3]) % 360) / 22.5)]
        wind_speed_in_knots = int(wind[3:5])
        wind_speed_in_mph = round(wind_speed_in_knots * 1.15078, 2)

        data = {'station': time_and_station[1],
                'last_observation': metar_data[0] + ' at ' + time_and_station[0] + ' GMT',
                'temperature': temperature_in_celsius + ' C (' + str(temperature_in_farhenheit) + ' F)',
                'wind': wind_direction + ' at ' + str(wind_speed_in_mph) + ' mph (' + str(
                    wind_speed_in_knots) + ' knots)'}
        cache.set(scode, data)
        return data