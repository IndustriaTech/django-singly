from django import template

from django_singly.api import singly

register = template.Library()


@register.simple_tag(takes_context=True)
def singly_login_url(context, service):
    """
    Get URL to which user must be redirected to authenticate with Singly

    If current user is already authenticated with singly
    We must pass his authenticetion token to oauth URL.
    Then Singly will know to connect two accounts from
    different services into one.
    """
    user = context.get('user')
    if user and user.is_authenticated():
        profile = user.get_profile()
        access_token = profile.singly_access_token
    else:
        access_token = None
    request = context.get('request')
    if request:
        next = request.GET.get('next')
    else:
        next = None
    return singly.get_authentication_url(service, access_token, next_url=next)
