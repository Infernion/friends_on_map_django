from django.core.cache import cache as memcache
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
        # FQL for friends is:
        #         SELECT uid, name,current_location.name, current_location.latitude, current_location.longitude
        #         FROM user WHERE uid IN(SELECT uid2 FROM friend WHERE uid1=me())
        friends = json.loads(urllib.urlopen(r'https://graph.facebook.com/fql?q=' \
                    'SELECT%20uid,name,current_location.name,current_location.latitude,current_location.longitude' \
                    '%20FROM%20user%20WHERE%20uid%20IN%20(SELECT%20uid2%20FROM%20friend%20WHERE%20uid1%20=%20me())' \
                    '&access_token={0}'.format(response['access_token'])).read())
        #location = response['location']
    if photo_url:
        social.set_extra_data({'photo': photo_url, 'friends': friends})


def get_data_vk(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    photo_url = None
    if strategy.backend.name == 'vk':


