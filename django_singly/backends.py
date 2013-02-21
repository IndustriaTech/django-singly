from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import get_model
from django.conf import settings

from .api import singly


def _get_names(name):
    try:
        first_name, last_name = name.split(' ')
    except ValueError:
        first_name, last_name = name, ''
    return first_name, last_name


class SinglyBackend(ModelBackend):
    profile_model = get_model(*settings.AUTH_PROFILE_MODULE.split('.'))

    def authenticate(self, singly_code):
        api = singly.authenticate(singly_code, profile='all', auth='true', full='true')
        if api:
            access_token = api.get_access_token()
            account = api.get_account()
            profile_data = api.get_profile()  # This will works because profile is set to 'all' or 'last'

            try:
                profile = self.profile_model.objects.select_related('user').get(account=account)
            except self.profile_model.DoesNotExist:
                email = profile_data.get('email') or ''
                user = None

                if email:
                    try:
                        user = User.objects.get(email=email)
                    except User.objects.DoesNotExist:
                        pass

                if not user:
                    first_name, last_name = _get_names(profile_data.get('name', ''))
                    user = User.objects.create(
                        username=account[:30],
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                    )

                try:
                    # If user is found by e-mail or there is a signal creating profile automaticaly
                    # then we try to get this profile
                    profile = user.get_profile()
                except self.profile_model.DoesNotExist:
                    # If it fails, then we create new profile
                    profile = self.profile_model(user=user)

            profile.account = account
            profile.singly_access_token = access_token
            profile.profile = profile_data
            profile.save()
            return profile.user
        return None
