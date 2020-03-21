#!/usr/bin/env python3
import os
import time

import prometheus_client

import logging
from airpurifier_mb3 import AirPurifierMB3

logger = logging.getLogger(__name__)


PURIFIER = AirPurifierMB3(os.environ['AIR_IP'], os.environ['AIR_TOKEN'], os.environ['AIR_DID'])


METRICS_INFO = {
    'pm25': (3, 6),
    'humidity_percent': (3, 7),
    'temp_celsius': (3, 8),
    'filter_life_percent': (4, 3),
    'motor_speed': (10, 8)
}

PROMETHEUS_VARS = {}


def init():
    for metric_name in METRICS_INFO:
        prom_var = prometheus_client.Gauge(metric_name, '', namespace='air_purifier')
        PROMETHEUS_VARS[metric_name] = prom_var


def update():
    metric_names = list(METRICS_INFO.keys())
    metric_info_list = [METRICS_INFO[x] for x in metric_names]
    metric_values = PURIFIER.get_prop_list(metric_info_list)

    for i in range(len(metric_names)):
        metric_name = metric_names[i]
        metric_value = metric_values[i]
        PROMETHEUS_VARS[metric_name].set(metric_value)


def main():
    logging.basicConfig(level=logging.INFO)
    init()

    listen_addr = os.getenv('LISTEN_ADDR', '')
    listen_port = int(os.getenv('LISTEN_PORT', 9134))
    prometheus_client.start_http_server(listen_port, listen_addr)

    while True:
        try:
            update()
        except Exception as ex:
            logger.error("Error getting data: %s", str(ex))
        time.sleep(4)


if __name__ == '__main__':
    main()
