
def get_user_avatar(strategy, details, response, social_user, uid,\
                    user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )

    url = None
    if strategy.backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    if url:
        social_user.set_extra_data({'photo': url})
    social.extra_data['test'] = 'test'
    social.save()
    user.set_extra_data['test'] = 'test'
    user.save()
    dfhd
    drh
    22fh