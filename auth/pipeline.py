from social.pipeline.social_auth import load_extra_data

def get_user_avatar(strategy, details, response, social_user, uid,\
                    user, *args, **kwargs):
    url = None
    if strategy.backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    if url:
        avatar = url
        social_user.set_extra_data({'photo': url})
