# -*- coding: utf-8 -*-

from django.core.cache import cache as memcache
import urllib
import json
import time

class Geocode(object):
    def get(self, address):
        """
        For convert address string to list geo data
        :type self: object
        :param address: like "city, country"
        :return: geodata [lat, lng]
        """
        format_address = "+".join(address.split())
        cached_coords = memcache.get('%s' % format_address)
        #cached_coords = None
        if cached_coords is not None:
            return cached_coords
        else:
            geodata = {u'status': u'', u'results': []}
            while not geodata['results']:
                geodata_json = urllib.urlopen(
                            url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %
                                format_address).read()
                geodata = json.loads(geodata_json)
                time.sleep(1)
            #print geodata
            try:
                geodata = geodata['results'][0]['geometry']['viewport']['northeast']
                coords = [geodata['lat'], geodata['lng']]
                memcache.set('%s' % format_address, coords)  # add new location to memcache
                return coords
            except IndexError:
                return [-82.471829, -118.857425]
