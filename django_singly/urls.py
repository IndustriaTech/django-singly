from django.conf.urls import patterns, url


urlpatterns = patterns('django_singly.views',
    url('^callback/$', 'callback', name='singly_callback'),
)
