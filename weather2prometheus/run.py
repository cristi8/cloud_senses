#!/usr/bin/env python3
import os
import time

import prometheus_client
import requests
import logging

logger = logging.getLogger(__name__)

# Required free api key
DARKSKY_API_KEY = os.environ['DARKSKY_API_KEY']

# Defaults to Bucharest, Romania
DARKSKY_GEO_NAME = os.getenv('DARKSKY_GEO_NAME', 'Bucharest')
DARKSKY_GEO_LOC = os.getenv('DARKSKY_GEO_LOC', '44.4268,26.1025')

# Defaults to SI system with km/h instead of m/s
# Other options: 'si', 'us'. More details: https://darksky.net/dev/docs
DARKSKY_UNITS = os.getenv('DARKSKY_UNITS', 'ca')

DARKSKY_QUERY_INTERVAL_MIN = int(os.getenv('DARKSKY_QUERY_INTERVAL_MIN', 3))


LISTEN_ADDR = os.getenv('LISTEN_ADDR', '')
LISTEN_PORT = int(os.getenv('LISTEN_PORT', 9133))


_example = {
    "time": 1574675977,
    "summary": "Foggy",
    "icon": "fog",
    "precipIntensity": 0.0036,
    "precipProbability": 0.19,
    "precipType": "rain",
    "temperature": 45.96,
    "apparentTemperature": 40.71,
    "dewPoint": 45.59,
    "humidity": 0.99,
    "pressure": 1017.6,
    "windSpeed": 10.88,
    "windGust": 18.51,
    "windBearing": 56,
    "cloudCover": 1,
    "uvIndex": 1,
    "visibility": 1.886,
    "ozone": 303.7
}

PROMETHEUS_VARS = {}

for k in _example.keys():
    try:
        float(_example[k])
    except Exception:
        continue
    if k in ['time']:
        continue
    PROMETHEUS_VARS[k] = prometheus_client.Gauge(k, k + ' variable', ['city'], namespace='crt_weather')


def darksky_get_weather(api_key, geoloc, units):
    url = 'https://api.darksky.net/forecast/%s/%s' % (api_key, geoloc)
    params = {
        'units': units,
        'exclude': 'minutely,hourly,daily,alerts,flags'
    }
    vars = requests.get(url, params=params).json()['currently']
    return vars


def update_weather():
    crt_vars = darksky_get_weather(DARKSKY_API_KEY, DARKSKY_GEO_LOC, DARKSKY_UNITS)
    for v in crt_vars.keys():
        if v not in PROMETHEUS_VARS:
            continue
        try:
            val = float(crt_vars[v])
        except Exception:
            continue
        PROMETHEUS_VARS[v].labels(DARKSKY_GEO_NAME).set(val)


def main():
    logging.basicConfig(level=logging.INFO)
    prometheus_client.start_http_server(LISTEN_PORT, LISTEN_ADDR)
    while True:
        try:
            update_weather()
        except Exception as ex:
            logger.error("Error getting weather data: %s", str(ex))
        time.sleep(DARKSKY_QUERY_INTERVAL_MIN * 60)


if __name__ == '__main__':
    main()
