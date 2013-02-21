from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import get_model

from open_singly import Singly, SinglyAPI

try:
    CALLBACK_URL = settings.SINGLY_CALLBACK_URL
except AttributeError:
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        site = get_model('sites', 'Site').objects.get_current()
        try:
            CALLBACK_URL = 'http://%s%s' % (site.domain, reverse('django_singly.views.callback'))
        except NoReverseMatch:
            raise ImproperlyConfigured('You must add django_singly.views.callback view into yur urls.py')
    else:
        raise ImproperlyConfigured('You must specify SINGLY_CALLBACK_URL in your settings or you must add django.contrib.sites in INSTALLED_APPS')


singly = Singly(settings.SINGLY_CLIENT_ID, settings.SINGLY_CLIENT_SECRET, CALLBACK_URL)


__all__ = ['singly', 'SinglyAPI']
