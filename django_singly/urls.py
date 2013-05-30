from django.conf.urls import patterns, url


urlpatterns = patterns('django_singly.views',
    url(r'^callback/$', 'callback', name='singly_callback'),
    url(r'^login/(?P<service>\w+)', 'login_redirect', name='singly_login')
)
