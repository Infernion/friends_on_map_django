from requests import request, HTTPError
from django.core.files.base import ContentFile

def save_picture(strategy, user, response, details,
                is_new=False, *args, **kwargs):

    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    user.set_extra_data({'photo_url': url})
