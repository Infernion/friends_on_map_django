def get_user_avatar(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    url = None
    if strategy.backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    if url:
        social.set_extra_data({'photo1': url})
    social.set_extra_data({'photo': 'photo'})
