from django.core.cache import cache as memcache
from urllib import urlencode
import urllib2
import json
import time


class GetVkData(object):
    """
    Args:
    code: Get var with auth code from vk.

    Returns:
    Auths user and redirects him to map page.
    """
    last_time = 0.0

    def __init__(self, uid, token):
        self.uid = uid
        self.token = token
        self.all_country = self.call_api((method="places.getCountryById",
                                          cids=",".join(map(str, range(236))))
    def get_country(self, id):
        """
        Taked id and return format country string
        :param id: current city id
        :return: string name
        """
        try:
            return self.all_country[int(id)-1]['name']
        except IndexError:
            return ""

    def get_city(self, id):
        """
        Take id and return format city string
        """
       # print "ID", id
        city = memcache.get('cid: %s' % id)
        if city is not None:
            return city
        else:
            try:
                get_city = (self.call_api(method="places.getCityById",
                                           cids=id))['name']
            except:
                return ""
            city = memcache.add('cid: %s' % id, get_city)
            return get_city

    def call_api(self, method, params):
        """
        This method formed QUERY with accepted parameter to VK API
        :param cids: for show country/city with id
        :param method: what query we do
        :param fields: what fields we will get
        :return: dict
        """
        time.sleep(max(0.0, 0.3333 - (time.clock() - last_time)))

        if isinstance(params, list):
                params_list = params[:]
        elif isinstance(params, dict):
                params_list = params.items()
        else:
                params_list = [params]

        params_list += [('access_token', .self.token)]
        url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params_list))

        response = urllib2.urlopen(url).read()
        last_time = time.clock()

        if method == "friends.get" or method == "places.getCountryById":
            try:
                return (json.loads(value_json))['response']  # If use get method return all item in value
            except IndexError:
                return ""
        try:
                return (json.loads(value_json))['response'][0]   # Else set first
        except IndexError:
            return ""

    def get_friends_from_json(self, user_friends):
        """
        Convert json values to namedtuple
        :user_friends: dict user friends
        :return: list of friends form: ['First_name Last_name', 'City, Country', city=bool, country=bool]
        """
        def format_address(field, city_id, country_id):
            city = self.get_city(field[city_id])
            country = self.get_country(field[country_id])
            address = '%s, %s' % (city, country)
            location = Geocode().get(address)
            return address, location

        def format(field, first_name, last_name):
            return '%s %s' % (field[first_name], field[last_name])

        friends = []
        for field in user_friends:
            if 'country' in field:
                if 'city' in field:
                    # Friends with city and country
                    friends.append({'name': format(field, 'first_name', 'last_name'),
                                    'address': format_address(field, 'city', 'country')[0],
                                    'location': format_address(field, 'city', 'country')[1],
                                    'uid': field['uid'], 'photo': field['photo'] })

                elif 'city' not in field:
                    friends.append({'name': (format(field, 'first_name', 'last_name')),
                                    'address': format_address(field, '', 'country')[0],
                                    'location': format_address(field, '', 'country')[1],
                                    'uid': field['uid'], 'photo': field['photo']})
            else:
            # Who haven't home
                friends.append({'name': (format(field, 'first_name', 'last_name')),
                                'address': 'Antarctica',
                                'location': '-82.471829,-118.857425',
                                'uid': field['uid'], 'photo': field['photo']})
        return friends
