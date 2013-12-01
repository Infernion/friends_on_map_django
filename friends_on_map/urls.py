from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('auth.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    #develop
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': '/home/infernion/Dev/friends_on_map/friends_on_map/static/'}),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': '/home/infernion/Dev/friends_on_map/friends_on_map/media'}),
)

