from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'friends_on_map.views.home', name='home'),
    # url(r'^friends_on_map/', include('friends_on_map.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('auth.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
