from urllib import urlencode
import urllib2
import json
import time
import logging
from urllib import quote, unquote_plus

#from django.core.cache import cache as memcache


class GetFacebookData(object):
    '''
    get: user id and token
    '''
    last_time = 0.0

    def __init__(self, uid, token):
        self.uid = uid
        self.token = token

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
        print 'p_list', params_list
        url = 'https://graph.facebook.com/%s?%s' % (method, unquote_plus(urlencode(params_list)))
        print 'facebook_url', url

        response = urllib2.urlopen(url).read()
        self.last_time = time.clock()

        return (json.loads(response))['data']  # If use get method return all item in value


#query = quote('SELECT uid, name,current_location.name, current_location.latitude, current_location.longitude '
#                   'FROM user WHERE uid IN(SELECT uid2 FROM friend WHERE uid1=me())', ',')
#print 'query', query
#get_data = GetFacebookData('CAADLGMaSz6ABAGt6WPm3u9Mae6U8ufCu20xZC5dgTvYR8T2BhtBFw3mK9sPt6noZBIodrFwvwIuRVy9eM4s7ZApf736dFx6VGNEm8Nb6PKXibZBsVKEtaK5ssZBrlZC1EThR2coqScmGMgnhQwwjmLRd2NVjnGH16yNT8NzjB9FcB7ZB5ZB6OdEx6FU52DN9f1AZD')
#print get_data.call_api('fql', {'q': query})
