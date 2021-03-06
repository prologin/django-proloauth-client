# Copyright (C) <2019> Association Prologin <association@prologin.org>
# SPDX-License-Identifier: GPL-3.0+

import requests

from django.conf import settings
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from proloauth_client import models
from proloauth_client.utils import handle_proloauth_response


class RefreshTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_anonymous:
            return

        try:
            token_infos = models.OAuthToken.objects.get(user=request.user)
        except models.OAuthToken.DoesNotExist:
            logout(request)
            return

        try:
            res = requests.post(
                '{}/refresh'.format(settings.OAUTH_ENDPOINT),
                json={
                    'refresh_token': token_infos.token,
                    'client_id': settings.OAUTH_CLIENT_ID,
                    'client_secret': settings.OAUTH_SECRET,
                },
            )
        except:
            return HttpResponseRedirect(reverse('proloauth_client:autologin'))

        if not handle_proloauth_response(request, res):
            return HttpResponseRedirect(reverse('proloauth_client:autologin'))
