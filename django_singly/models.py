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

    @property
    def services(self):
        return self.profile['services'].keys()

    @property
    def singly(self):
        if not self.singly_access_token:
            return
        if not hasattr(self, '_singly_cache'):
            self._singly_cache = SinglyAPI(self.singly_access_token)
        return self._singly_cache

    def __unicode__(self):
        return "Profile for '%s'" % self.user


class SinglyProfile(SinglyProfileBase):
    user = models.OneToOneField(User, related_name='singly')
