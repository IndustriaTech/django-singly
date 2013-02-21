from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from json_field import JSONField
from open_singly import SinglyAPI


class SinglyProfileBase(models.Model):
    account = models.CharField(max_length=255, blank=True, default='', db_index=True)
    singly_access_token = models.CharField(max_length=512, blank=True, default='')
    profile = JSONField(blank=True, default={})

    class Meta:
        abstract = True

    def __unicode__(self):
        return "Profile for '%s'" % self.user

    @property
    def services(self):
        """
        Return list of services for given user

        """
        return self.profile.get('services', {}).keys()

    @property
    def singly(self):
        """
        Property which returns a SinglyAPI object for current user

        """
        if not self.singly_access_token:
            return
        if not hasattr(self, '_singly_cache'):
            self._singly_cache = SinglyAPI(self.singly_access_token)
        return self._singly_cache


if settings.AUTH_PROFILE_MODULE == 'django_singly.SinglyProfile':

    class SinglyProfile(SinglyProfileBase):
        """
        Singly profiles will be stored here if AUTH_PROFILE_MODULE
        is set to this model. In other cases you must extend a
        SinglyProfileBase and add user field with foreign key to User
        """
        user = models.OneToOneField(User, related_name='singly', editable=False)
