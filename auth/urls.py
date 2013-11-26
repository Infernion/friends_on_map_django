from django.conf.urls import patterns, url
from auth import views

urlpatterns = patterns('',
        # url(r'^signup-email/', views.signup_email),
        # url(r'^email-sent/', views.validation_sent),
        url(r'^login/$', views.login, name='login'),
        url(r'^done/$', views.done, name='done'),
        # url(r'^email/$', views.require_email, name='require_email'),
        #url('', views.home),
        url(r'^about/$', views.about),
)