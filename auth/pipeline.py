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
        social.set_extra_data({'photo': url})
        social.save()
    social.set_extra_data({'photo': url})
    social.save()

def load_extra_data(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    if social:
        extra_data = strategy.backend.extra_data(user, uid, response, details)
        social.set_extra_data(extra_data)
        social.set_extra_data({'test':'test'})
