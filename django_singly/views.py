from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.conf import settings

SINGLY_CALLBACK_REDIRECT = getattr(settings, 'SINGLY_CALLBACK_REDIRECT', '/')
SINGLY_CALLBACK_FAIL_REDIRECT = getattr(settings, 'SINGLY_CALLBACK_FAIL_REDIRECT', '/login/fail/')
SINGLY_CALLBACK_ERROR_REDIRECT = getattr(settings, 'SINGLY_CALLBACK_ERROR_REDIRECT', '/login/error/')


def callback(request):
    if 'error' in request.GET:
        # TODO: send a message to user with error
        return HttpResponseRedirect(SINGLY_CALLBACK_ERROR_REDIRECT)
    code = request.GET.get('code')
    if code:
        user = authenticate(singly_code=code)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(SINGLY_CALLBACK_REDIRECT)
    return HttpResponseRedirect(SINGLY_CALLBACK_FAIL_REDIRECT)
