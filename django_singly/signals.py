from django.dispatch import Signal

singly_user_registered = Signal(providing_args=['user', 'profile_data'])

singly_profile_pre_update = Signal(providing_args=['user', 'profile', 'profile_data'])

singly_profile_post_update = Signal(providing_args=['user', 'profile', 'profile_data'])
