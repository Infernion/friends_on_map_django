import urllib

def get_user_friends(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    if social:
        extra_data = strategy.backend.extra_data(user, uid, response, details, 'test')
        social.set_extra_data(extra_data)