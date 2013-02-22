from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import get_model
from django.conf import settings

from .api import singly, NEW_USERS_ARE_ACTIVE
from signals import singly_user_registered, singly_profile_pre_update, singly_profile_post_update


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
                created = False
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

                if created:
                    singly_user_registered.send(sender=User, user=user, profile_data=profile_data)

            singly_profile_pre_update.send(sender=User, user=profile.user, profile=profile, profile_data=profile_data)

            profile.account = account
            profile.singly_access_token = access_token
            profile.profile = profile_data
            profile.save()

            singly_profile_post_update.send(sender=User, user=profile.user, profile=profile, profile_data=profile_data)
            return profile.user
        return None
