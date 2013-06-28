from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import get_model
from django.conf import settings

from .api import singly, NEW_USERS_ARE_ACTIVE, UPDATE_EMAIL_ON_LOGIN
from signals import singly_user_registered, singly_profile_pre_update, singly_profile_post_update


def _get_names(name):
    try:
        first_name, last_name = name.split(' ', 1)
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

            profile, created = self.get_profile(account, profile_data)

            if created:
                singly_user_registered.send(sender=User, user=profile.user, profile_data=profile_data)

            singly_profile_pre_update.send(sender=User, user=profile.user, profile=profile, profile_data=profile_data)

            profile.account = account
            profile.singly_access_token = access_token
            profile.profile = profile_data
            profile.save()

            user = profile.user

            if UPDATE_EMAIL_ON_LOGIN and profile_data.get('email'):
                # We don't need to save the user because backend will save it
                # when update last login date
                user.email = profile_data['email']

            singly_profile_post_update.send(sender=User, user=user, profile=profile, profile_data=profile_data)
            return user
        return None

    def get_profile(self, account, profile_data=None):
        """
        Try to get profile from the database

        Returns tuple containing profile object and boolean indicates if user is new or no

        """
        try:
            profile = self.profile_model.objects.select_related('user').get(account=account)
        except self.profile_model.DoesNotExist:
            pass
        else:
            return profile, False

        profile_data = profile_data or {}
        user = self.find_user(profile_data)

        created = False
        if not user:
            first_name, last_name = _get_names(profile_data.get('name', ''))
            email = profile_data.get('email') or ''
            user = User.objects.create(
                username=account[:30],
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=NEW_USERS_ARE_ACTIVE,
            )
            created = True

        try:
            # If user is found by e-mail or there is a signal creating profile automaticaly
            # then we try to get this profile
            profile = user.get_profile()
        except self.profile_model.DoesNotExist:
            # If it fails, then we create new profile
            profile = self.profile_model(user=user)

        return profile, created

    def find_user(self, profile_data):
        """
        Try to get user matching some criteria.
        By default we can try to match by e-mail address.

        This method can be overwritten to search by extra criteria

        """
        email = profile_data.get('email') or ''
        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                pass
