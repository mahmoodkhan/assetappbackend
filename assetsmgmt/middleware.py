import time
from random import random, randint

from django.db.models import signals
from django.utils.functional import curry

from django.conf import settings

class DelayResponse(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if settings.DRF_DELAY_ENABLED == True:
            time.sleep(randint(0,1))
        return response


class WhoDoneItMiddleware(object):
    """
    Populate created_by and updated_by foreign key refs to any model automatically.
    Almost completely taken from:
        https://github.com/Atomidata/django-audit-log/blob/master/audit_log/middleware.py

    This is how to make it work with RestFramework wihtout using session:
        from rest_framework import authentication

        try:
            user = request.user
            if not user.is_authenticated():
                auth = authentication.BasicAuthentication().authenticate(request)
                if auth:
                    user = auth[0]
                else:
                    user = None
        except (authentication.exceptions.AuthenticationFailed, KeyError):
            user = None
    """

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated():
                user = request.user.userprofile
            else:
                user = None

            mark_whodoneit = curry(self.mark_whodoneit, user)
            signals.pre_save.connect(mark_whodoneit,  dispatch_uid = (self.__class__, request,), weak = False)

        response = self.get_response(request)
        signals.pre_save.disconnect(dispatch_uid =  (self.__class__, request,))
        return response

    def mark_whodoneit(self, user, sender, instance, **kwargs):
        if not getattr(instance, 'created_by_id', None):
            instance.created_by = user
        if hasattr(instance,'updated_by_id'):
            if instance.pk:
                instance.updated_by = user

