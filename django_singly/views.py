from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.conf import settings

CALLBACK_REDIRECT = getattr(settings, 'SINGLY_CALLBACK_REDIRECT', '/')
CALLBACK_FAIL_REDIRECT = getattr(settings, 'SINGLY_CALLBACK_FAIL_REDIRECT', '/login/fail/')
CALLBACK_ERROR_REDIRECT = getattr(settings, 'SINGLY_CALLBACK_ERROR_REDIRECT', '/login/error/')


def callback(request):
    if 'error' in request.GET:
        # TODO: send a message to user with error
        return HttpResponseRedirect(CALLBACK_ERROR_REDIRECT)
    code = request.GET.get('code')
    if code:
        user = authenticate(singly_code=code)
        if user is not None:
            login(request, user)
            next = request.GET.get('next') or CALLBACK_REDIRECT
            return HttpResponseRedirect(next)
    return HttpResponseRedirect(CALLBACK_FAIL_REDIRECT)


def login_redirect(request, service):
    # This import prevents circular import if SINGLY_CALLBACK_URL is not set
    from .api import singly

    user = request.user
    next = request.REQUEST.get('next') or request.get_full_path()
    if user.is_authenticated():
        profile = user.get_profile()
        access_token = profile.singly_access_token
    else:
        access_token = None
    url = singly.get_authentication_url(service, access_token, next_url=next)
    return HttpResponseRedirect(url)
