from requests import request, HTTPError
from django.core.files.base import ContentFile


def save_picture(strategy, user, response, details,
                is_new=False, *args, **kwargs):

    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    user.set_extra_data({'photo_url': url})


def load_extra_data(strategy, details, response, uid, user, is_new=False, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    if social:
        #if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        extra_data = strategy.backend.extra_data(user, uid, response, details, url)
        social.set_extra_data(extra_data)