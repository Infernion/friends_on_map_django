# -*- coding: utf-8 -*-
import urllib
import json


def get_data_fb(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    photo_url = None
    if strategy.backend.name == 'facebook':
        photo_url = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
        friends = json.loads(urllib.urlopen(r'https://graph.facebook.com/fql?q=SELECT%20name,uid,' \
                  r'current_location.latitude,current_location.longitude' \
                  r'%20FROM%20user%20WHERE%20uid%20IN%20(SELECT%20uid2%20FROM%20friend%20WHERE%20uid1%20=%20me())' \
                  '&access_token={0}'.format(response['access_token'])))

    if photo_url:
        social.set_extra_data({'photo': photo_url})
    social.set_extra_data({'test1':'test'})

def get_data_vk(strategy, details, response, uid, user, *args, **kwargs):
    pass