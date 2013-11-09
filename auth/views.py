from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

def login(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return render_to_response('login.html', {
        'vk_uid': getattr(settings, 'SOCIAL_AUTH_VK_OAUTH2_KEY', None),
        'fb_uid': getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', None)
    }, RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    request.user.set_extra_data('test')
    return render_to_response('done.html', {
        'user': request.user,
        'vk_uid': getattr(settings, 'SOCIAL_AUTH_VK_OAUTH2_KEY', None),
        'fb_uid': getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', None),
    }, RequestContext(request))

def home(request):
    pass
    