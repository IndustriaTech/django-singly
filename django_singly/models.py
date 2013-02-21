from django.db import models
from django.contrib.auth.models import User

from json_field import JSONField
from open_singly import SinglyAPI


class SinglyProfileBase(models.Model):
    account = models.CharField(max_length=255, unique=True)
    singly_access_token = models.CharField(max_length=512)
    profile = JSONField()

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


class SinglyProfile(SinglyProfileBase):
    user = models.OneToOneField(User, related_name='singly')
