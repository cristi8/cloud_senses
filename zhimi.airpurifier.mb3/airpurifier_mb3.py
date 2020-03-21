import miio
import logging

logger = logging.getLogger(__name__)

# Services and Properties for this device can be found at:
# https://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:air-purifier:0000A007:zhimi-mb3:1


class AirPurifierMB3(object):
    def __init__(self, device_ip, device_token, did):
        self.did = did
        self.miio_device = miio.Device(device_ip, device_token)

    def get_prop(self, service_iid, property_iid):
        result = self.miio_device.raw_command(
            'get_properties',
            [
                {
                    'did': str(self.did),
                    'siid': int(service_iid),
                    'piid': int(property_iid)
                }
            ]
        )
        return result[0]['value']

    def get_prop_list(self, list_of_siid_piid):
        results = self.miio_device.raw_command(
            'get_properties', [{'did': str(self.did), 'siid': int(x[0]), 'piid': int(x[1])} for x in list_of_siid_piid]
        )
        return [x['value'] for x in results]
