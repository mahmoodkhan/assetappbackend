import time
from random import random, randint

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