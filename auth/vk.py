# -*- coding: utf-8 -*-
from urllib import urlencode
import urllib2
import json
import time
import logging
from geocode import Geocode

from django.utils.encoding import smart_str, smart_unicode
from django.core.cache import cache as memcache


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
#log.py[LINE:33]# DEBUG    [2012-05-25 00:11:58,466]  This is a debug message
#log.py[LINE:34]# INFO     [2012-05-25 00:11:58,466]  This is an info message
#log.py[LINE:35]# WARNING  [2012-05-25 00:11:58,466]  This is a warning
#log.py[LINE:36]# ERROR    [2012-05-25 00:11:58,467]  This is an error message
#log.py[LINE:37]# CRITICAL [2012-05-25 00:11:58,467]  FATAL!!!


class GetVkData(object):
    '''
    Args:
    code: Get var with auth code from vk.

    Returns:
    Auths user and redirects him to map page.
    '''
    last_time = 0.0

    def __init__(self, uid, token):
        self.uid = uid
        self.token = token
        self.all_country = self.call_api('places.getCountryById', {'cids': ','.join(map(str, range(236)))})
        #logging.info(self.all_country)

    def get_country(self, id):
        '''
        Taked id and return format country string
        :param id: current city id
        :return: string name
        '''
        try:
            return self.all_country[int(id) - 1]['name']
        except IndexError:
            return ''

    def get_city(self, id):
        '''
        Take id and return format city string
        '''
        # print 'ID', id
        city = memcache.get('cid: %s' % id)
        #logging.warning(id)
        #logging.warning(city)
        #city = None
        if city is not None:
            return city
        else:
            #try:
            get_city =((self.call_api('places.getCityById', {'cids': id}))['name']).encode(encoding='utf-8')
            #logging.warning(get_city)
            #except IndexError:
            #    return ''
            memcache.set('cid: %s' % id, get_city)
            #logging.warning('after_try')
            return get_city

    def call_api(self, method, params):
        '''
        This method formed QUERY with accepted parameter to VK API
        :param cids: for show country/city with id
        :param method: what query we do
        :param fields: what fields we will get
        :return: dict
        '''
        time.sleep(max(0.0, 0.3333 - (time.clock() - self.last_time)))

        if isinstance(params, list):
            params_list = params[:]
        elif isinstance(params, dict):
            params_list = params.items()
        else:
            params_list = [params]

        params_list += [('access_token', self.token)]
        url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params_list))

        response = urllib2.urlopen(url).read()
        self.last_time = time.clock()
        #print (json.loads(response))
        if method == 'friends.get' or method == 'places.getCountryById':
            try:
                return (json.loads(response))['response']  # If use get method return all item in value
            except IndexError:
                return ''
        try:
            return (json.loads(response))['response'][0]   # Else set first
        except IndexError:
            return ''

    def get_friends_from_json(self, user_friends):
        '''
        Convert json values to namedtuple
        :user_friends: dict user friends
        :return: list of friends form: ['First_name Last_name', 'City, Country', city=bool, country=bool]
        '''
        friends = []
        #logging.warning(user_friends)
        for field in user_friends:
            if 'country' in field:
                if 'city' in field:
                    # Friends with city and country
                    #logging.warning('city_in_field')
                    #logging.warning(field)
                    friends.append({'name': self.format(field, 'first_name', 'last_name'),
                                    'current_location': {
                                        'name': self.format_address(field, 'city', 'country')[0],
                                        'latitude': self.format_address(field, 'city', 'country')[1][0],
                                        'longitude': self.format_address(field, 'city', 'country')[1][1]},
                                    'uid': field['uid'], 'pic_square': field['photo']})
                elif 'city' not in field:
                    #logging.warning('city_not_in_field')
                    friends.append({'name': self.format(field, 'first_name', 'last_name'),
                                    'current_location': {
                                        'name': self.format_address(field, '', 'country')[0],
                                        'latitude': self.format_address(field, '', 'country')[1][0],
                                        'longitude': self.format_address(field, '', 'country')[1][1]},
                                    'uid': field['uid'], 'photo': field['photo']})
            else:
            # Who haven't home
                friends.append({'name': (self.format(field, 'first_name', 'last_name')),
                                'current_location': {
                                    'name': 'Antarctica',
                                    'latitude': '-82.471829',
                                    'longitude': '-118.857425'},
                                'uid': field['uid'], 'photo': field['photo']})
        return friends

    def format_address(self, field, city_id, country_id):
        city = self.get_city(field[city_id])
        try:
            city.encode()
        except:
            pass
        country = self.get_country(field[country_id])
        address = '%s, %s' % (city, country.encode())
        #logging.warning(field[city_id])
        #logging.warning(city)
        #logging.warning(country)
        #logging.warning(address)
        location = Geocode().get(address)
        return address, location

    def format(self, field, first_name, last_name):
        return '%s %s' % (field[first_name], field[last_name])

#get_data = GetVkData('15826446', '1b23f473a03c478b3c430f8f60a067624c2804725446f38440cd41e251c
# eac574d6828e76c9ea1c1f431d')
#friends = get_data.call_api('friends.get', {'fields': 'uid,first_name,last_name,country,city,photo'})
#print friends
#print 'user_info', user_info
#user_info_formated = {'name': get_data.format(user_info, 'first_name', 'last_name'),
#                             'current_location': {
#                                'name': get_data.format_address(user_info, 'city', 'country')[0],
#                                'latitude': get_data.format_address(user_info, 'city', 'country')[1][0],
#                                'longitude': get_data.format_address(user_info, 'city', 'country')[1][1]},
#                            'uid': user_info['uid'], 'pic_big': user_info['photo_max']}
#print  user_info_formated