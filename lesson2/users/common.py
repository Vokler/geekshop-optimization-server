from django.contrib.gis.geoip2 import GeoIP2
from ipware import get_client_ip


def get_user_location(request):
    client_ip, routable = get_client_ip(request)
    g = GeoIP2()
    # location = g.city(client_ip)
    location = g.city('77.138.3.215')
    return location
