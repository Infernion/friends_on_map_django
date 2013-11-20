import urllib
import json
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
#log.py[LINE:33]# DEBUG    [2012-05-25 00:11:58,466]  This is a debug message
#log.py[LINE:34]# INFO     [2012-05-25 00:11:58,466]  This is an info message
#log.py[LINE:35]# WARNING  [2012-05-25 00:11:58,466]  This is a warning
#log.py[LINE:36]# ERROR    [2012-05-25 00:11:58,467]  This is an error message
#log.py[LINE:37]# CRITICAL [2012-05-25 00:11:58,467]  FATAL!!!


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
    user_info, user_friends = None, None
    logging.DEBUG('test')
    if strategy.backend.name == 'vkontakte':
        logging.DEBUG('vkontakte section')
        from vk import GetVkData
        social = kwargs.get('social') or strategy.storage.user.get_social_auth(
            strategy.backend.name,
            uid
        )
        get_data = GetVkData(response['id'], response['access_token']) # uid, token
        user_info = get_data.call_api('users.get', {'fields': 'city,country,photo_rec'})
        user_friends = get_data.call_api('friends.get', {'fields': 'uid,first_name,last_name,country,city,photo'})
    if strategy.backend.name == 'vk':
        logging.DEBUG('vk section')
        from vk import GetVkData
        social = kwargs.get('social') or strategy.storage.user.get_social_auth(
            strategy.backend.name,
            uid
        )
        get_data = GetVkData(response['id'], response['access_token']) # uid, token
        user_info = get_data.call_api('users.get', {'fields': 'city,country,photo_rec'})
        user_friends = get_data.call_api('friends.get', {'fields': 'uid,first_name,last_name,country,city,photo'})
    if user_info and user_friends:
        social.set_extra_data({'user_data': user_info, 'friends': user_friends})



