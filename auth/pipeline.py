import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
#log.py[LINE:33]# DEBUG    [2012-05-25 00:11:58,466]  This is a debug message
#log.py[LINE:34]# INFO     [2012-05-25 00:11:58,466]  This is an info message
#log.py[LINE:35]# WARNING  [2012-05-25 00:11:58,466]  This is a warning
#log.py[LINE:36]# ERROR    [2012-05-25 00:11:58,467]  This is an error message
#log.py[LINE:37]# CRITICAL [2012-05-25 00:11:58,467]  FATAL!!!


def get_data_fb(strategy, details, response, uid, user, *args, **kwargs):
    user_info, friends = None, None
    if strategy.backend.name == 'facebook':
        from urllib import quote
        from facebook import GetFacebookData

        social = kwargs.get('social') or strategy.storage.user.get_social_auth(
            strategy.backend.name, uid)
        get_data = GetFacebookData(response['id'], response['access_token'])
        user_info = get_data.call_api('fql',
                                      {'q': quote('SELECT uid,name,current_location.name, current_location.latitude, '
                                                  'current_location.longitude, pic_big, profile_url, friend_count '
                                                  'FROM user WHERE uid=me()', ',')})

        friends = get_data.call_api('fql',
                                    {'q': quote('SELECT uid, name,current_location.name, current_location.latitude, '
                                                'current_location.longitude, pic_square, profile_url '
                                                'FROM user WHERE uid IN(SELECT uid2 FROM friend WHERE uid1=me())',
                                                ',')})
        if user_info and friends:
            social.set_extra_data({'friends': friends, 'user_info': user_info[0]})


def get_data_vk(strategy, details, response, uid, user, *args, **kwargs):
    user_info_formated, friends_formated = None, None
    if strategy.backend.name == 'vk-oauth2':
        from vk import GetVkData

        social = kwargs.get('social') or strategy.storage.user.get_social_auth(
            strategy.backend.name, uid)
        get_data = GetVkData(response['uid'], response['access_token'])
        friends = get_data.call_api('friends.get', {'fields': 'uid,first_name,last_name,country,city,photo'})
        print 'friends', friends
        friends_formated = get_data.get_friends_from_json(friends)
        print 'friends_formated', friends_formated
        user_info = get_data.call_api('user.get', {'fields': 'uid,first_name,last_name,country,city,photo_max'})
        print 'user_info', user_info
        user_info_formated = {'name': self.format(user_info, 'first_name', 'last_name'),
                             'current_location': {
                                'name': self.format_address(user_info, 'city', 'country')[0],
                                'latitude': self.format_address(user_info, 'city', 'country')[1][0],
                                'longitude': self.format_address(user_info, 'city', 'country')[1][1]},
                            'uid': user_info['uid'], 'pic_big': user_info['photo_max']}
        print 'user_info_formated', user_info_formated
    if user_info_formated and friends_formated:
        social.set_extra_data({'user_info': user_info_formated[0], 'friends': friends_formated})



