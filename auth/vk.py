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
        city = None
        city = memcache.get('cid: %s' % id)
        #logging.warning(id)
        #logging.warning(city)
        if city is not None:
            return city
        else:
            try:
                get_city =((self.call_api('places.getCityById', {'cids': id}))['name']).encode(encoding='utf-8')
            #logging.warning(get_city)
            except:
                return ''
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
            except IndexError or KeyError:
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
        for field in user_friends:
            data = memcache.get('f_data: %s' % field['uid'])
            if data is not None:
                logging.warning('from_chache %s' % data )
                friends.append(data)
            if 'country' in field:
                if 'city' in field:
                    # Friends with city and country
                    #logging.warning('city_in_field')

                    #logging.warning(field)
                    data = {'name': self.format(field, 'first_name', 'last_name'),
                                    'current_location': {
                                        'name': self.format_address(field, 'city', 'country')[0],
                                        'latitude': self.format_address(field, 'city', 'country')[1][0],
                                        'longitude': self.format_address(field, 'city', 'country')[1][1]},
                                    'uid': field['uid'], 'pic_square': field['photo']}
                    memcache.set('f_data: %s' % field['uid'], data)
                    friends.append(data)
                elif 'city' not in field:
                    #logging.warning('city_not_in_field')
                    data = {'name': self.format(field, 'first_name', 'last_name'),
                                    'current_location': {
                                        'name': self.format_address(field, '', 'country')[0],
                                        'latitude': self.format_address(field, '', 'country')[1][0],
                                        'longitude': self.format_address(field, '', 'country')[1][1]},
                                    'uid': field['uid'], 'photo': field['photo']}
                    friends.append(data)
                    memcache.set('f_data: %s' % field['uid'], data)
            else:
            # Who haven't home
                friends.append({'name': (self.format(field, 'first_name', 'last_name')),
                                'current_location': {
                                    'name': 'Antarctica',
                                    'latitude': '-82.471829',
                                    'longitude': '-118.857425'},
                                'uid': field['uid'], 'photo': field['photo']})
        logging.warning(friends)
        return friends

    def format_address(self, field, city_id, country_id):
        city = self.get_city(field[city_id])
        try:
            city = city.encode(encoding='utf-8')
        except:
            pass
        country = self.get_country(field[country_id])
        address = '%s, %s' % (city, country.encode(encoding='utf-8'))
        #logging.warning(field[city_id])
        #logging.warning(city)
        #logging.warning(country)
        #logging.warning(address)
        location = Geocode().get(address)
        return address, location

    def format(self, field, first_name, last_name):
        return '%s %s' % (field[first_name], field[last_name])

#get_data = GetVkData('15826446', '1b23f473a03c478b3c430f8f60a067624c2804725446f38440cd41e251ceac574d6828e76c9ea1c1f431d')
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

#friends = [{u'lists': [5], u'uid': 785264, u'photo': u'http://cs301201.vk.me/v301201264/5dd9/QBIig3KKWec.jpg', u'online': 1, u'first_name': u'Art', u'user_id': 785264, u'last_name': u'Rudenko', u'city': u'2', u'country': u'1'},
#           {u'lists': [2], u'uid': 2004404, u'photo': u'http://cs9230.vk.me/v9230404/b3a/jNzstepiPpI.jpg', u'online': 1, u'first_name': u'Denis', u'user_id': 2004404, u'last_name': u'Kvitka', u'city': u'314', u'country': u'2'},
#           {u'lists': [2], u'uid': 3275028, u'photo': u'http://cs425929.vk.me/v425929028/305d/VQMQFLMrd_U.jpg', u'online': 0, u'first_name': u'Flying', u'user_id': 3275028, u'last_name': u'Buddha', u'city': u'0', u'country': u'0'},
#           {u'lists': [2], u'uid': 3811114, u'photo': u'http://cs424921.vk.me/v424921114/401b/TIdAoyVq8rQ.jpg', u'online': 0, u'first_name': u'Zhanna', u'user_id': 3811114, u'last_name': u'Khveschuk', u'city': u'314', u'country': u'2'},
#           {u'lists': [29], u'uid': 3962539, u'photo': u'http://cs313124.vk.me/v313124539/3810/OtKXy3WrbOY.jpg', u'online': 0, u'first_name': u'Dimon', u'user_id': 3962539, u'last_name': u'Gritsenko', u'city': u'15401', u'country': u'2'},
#           {u'uid': 3966779, u'photo': u'http://cs301810.vk.me/v301810779/57f3/riKR-kP5PUk.jpg', u'online': 0, u'first_name': u'Nazar', u'user_id': 3966779, u'last_name': u'Kaznadzey', u'city': u'314', u'country': u'2'},
#           {u'lists': [2], u'uid': 4521227, u'photo': u'http://cs9622.vk.me/u4521227/e_8e988e64.jpg', u'online': 0, u'first_name': u'Andrey', u'user_id': 4521227, u'last_name': u'Kovtunov', u'city': u'0', u'country': u'0'},
#           {u'lists': [2], u'uid': 5734365, u'photo': u'http://cs417317.vk.me/v417317365/c921/wN8DBbo0PdI.jpg', u'online': 0, u'first_name': u'Valentina', u'user_id': 5734365, u'last_name': u'Teslenko', u'city': u'314', u'country': u'2'},
#           {u'lists': [2], u'uid': 5744690, u'photo': u'http://cs413318.vk.me/v413318690/5483/IjSjtOffov4.jpg', u'online': 0, u'first_name': u'Anton', u'user_id': 5744690, u'last_name': u'Porkhun', u'city': u'123', u'country': u'1'},
#           {u'lists': [2], u'uid': 5815305, u'photo': u'http://cs409124.vk.me/v409124305/6074/w5x1EpIcTOo.jpg', u'online': 0, u'first_name': u'Stella', u'user_id': 5815305, u'last_name': u'Melnichenko', u'city': u'314', u'country': u'2'},
#           {u'uid': 6071130, u'photo': u'http://cs616629.vk.me/v616629130/3148/QsGvbyvA4vw.jpg', u'online': 0, u'first_name': u'Yury', u'user_id': 6071130, u'last_name': u'Gugnin', u'city': u'280', u'country': u'2'},
#           {u'lists': [2], u'uid': 6488136, u'photo': u'http://cs425923.vk.me/v425923136/1286/X3MGyWpIyts.jpg', u'online': 0, u'first_name': u'Sergey', u'user_id': 6488136, u'last_name': u'Kushpela', u'city': u'314', u'country': u'2'},
#           {u'lists': [2], u'uid': 6820564, u'photo': u'http://cs424128.vk.me/v424128564/3ade/oUniG8N57yw.jpg', u'online': 0, u'first_name': u'Grigory', u'user_id': 6820564, u'last_name': u'Krolivets', u'city': u'375', u'country': u'3'},
#           {u'lists': [26], u'uid': 7528815, u'photo': u'http://cs413723.vk.me/v413723815/3ccc/sSjFIfwrc3s.jpg', u'online': 0, u'first_name': u'Ekaterina', u'user_id': 7528815, u'last_name': u'Khalymon', u'city': u'314', u'country': u'2'},
#           {u'lists': [2], u'uid': 7533663, u'photo': u'http://cs416822.vk.me/v416822663/8ab7/WxQcWRe3Vlo.jpg', u'online': 0, u'first_name': u'Artyom', u'user_id': 7533663, u'last_name': u'Larkov', u'city': u'665', u'country': u'2'},
#           {u'lists': [2], u'uid': 7684768, u'photo': u'http://cs7001.vk.me/c320222/v320222768/4e39/nu7ETNEvYi4.jpg', u'online': 0, u'first_name': u'Alexander', u'user_id': 7684768, u'last_name': u'Efimenko', u'city': u'314', u'country': u'2'},
#           {u'uid': 8121430, u'photo': u'http://cs11191.vk.me/u8121430/e_9ddf90cc.jpg', u'online': 0, u'first_name': u'Seryoga', u'user_id': 8121430, u'last_name': u'Steshkin', u'city': u'280', u'country': u'2'},
#           {u'uid': 8164626, u'photo': u'http://cs312524.vk.me/v312524626/1097/aOjbKVea_js.jpg', u'online': 0, u'first_name': u'Lesik', u'user_id': 8164626, u'last_name': u'Kopa', u'city': u'15401', u'country': u'2'},
#           {u'lists': [2], u'uid': 8314006, u'photo': u'http://cs407127.vk.me/v407127006/7c1c/mQ1iJZyNXYU.jpg', u'online': 0, u'first_name': u'Sergey', u'user_id': 8314006, u'last_name': u'Zverev', u'city': u'314', u'country': u'2'},
#           {u'lists': [8], u'uid': 8924619, u'photo': u'http://cs411426.vk.me/v411426619/a980/dYoOtaDuBq0.jpg', u'online': 0, u'first_name': u'Alexey', u'user_id': 8924619, u'last_name': u'Kolesnikov', u'city': u'280', u'country': u'2'},
#           {u'lists': [2], u'uid': 8924674, u'photo': u'http://cs410327.vk.me/v410327674/a6da/FQjCKQWCTNA.jpg', u'online': 0, u'first_name': u'Pavel', u'user_id': 8924674, u'last_name': u'Mintyan', u'city': u'314', u'country': u'2'},
#           {u'uid': 8965996, u'photo': u'http://cs5222.vk.me/u8965996/e_04515cea.jpg', u'online': 0, u'first_name': u'Ruslan', u'user_id': 8965996, u'last_name': u'Marusenko', u'city': u'0', u'country': u'2'},
#           {u'lists': [2], u'uid': 9040945, u'photo': u'http://cs313229.vk.me/v313229945/4fb9/UijHiTUi6tE.jpg', u'online': 0, u'first_name': u'Anechka', u'user_id': 9040945, u'last_name': u'Khatimlyanskaya', u'city': u'314', u'country': u'2'},
#           {u'lists': [9], u'uid': 9195148, u'photo': u'http://cs616130.vk.me/v616130148/224/69nLk_1KVh8.jpg', u'online': 0, u'first_name': u'Bagrat', u'user_id': 9195148, u'last_name': u'Saatsazov', u'city': u'0', u'country': u'0'},
#           {u'uid': 9483398, u'photo': u'http://cs5201.vk.me/u9483398/e_cf5ac768.jpg', u'online': 1, u'first_name': u'Vitaly', u'user_id': 9483398, u'last_name': u'Puzirenko', u'city': u'314', u'country': u'2'},
#           {u'uid': 9487161, u'photo': u'http://cs418319.vk.me/v418319161/8439/DN2mHiOK5Fg.jpg', u'online': 1, u'first_name': u'Yaroslav', u'user_id': 9487161, u'last_name': u'Dorosh', u'city': u'0', u'country': u'2'}]
#get_data.get_friends_from_json(friends)