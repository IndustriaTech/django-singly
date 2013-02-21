from django.contrib import admin
from django.db.models import get_model
from django.conf import settings


class SinglyProfiileAdmin(admin.ModelAdmin):
    read_only_fields = ['user', 'services']
    list_display = ['user', 'account', 'services', 'singly_access_token']

if settings.AUTH_PROFILE_MODULE == 'django_singly.SinglyProfile':
    admin.site.register(get_model(settings.AUTH_PROFILE_MODULE), SinglyProfiileAdmin)
