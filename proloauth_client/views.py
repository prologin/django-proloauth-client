# Copyright (C) <2019> Association Prologin <association@prologin.org>
# SPDX-License-Identifier: GPL-3.0+

import os
import requests
from urllib.parse import urlencode

from django.conf import settings
from django.views.generic import RedirectView

from proloauth_client.utils import handle_proloauth_response, gen_auth_state


class AutoLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.request.session['proloauth_state'] = gen_auth_state()
        request_params = {
            'client_id': settings.OAUTH_CLIENT_ID,
            'state': self.request.session['proloauth_state'],
        }

        if 'next' in self.request.GET:
            request_params.update({'next': self.request.GET['next']})

        return '{}/authorize?{}'.format(
            settings.OAUTH_ENDPOINT, urlencode(request_params)
        )


class Callback(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = settings.LOGIN_REDIRECT_URL

        if 'next' in self.request.GET:
            url = os.path.join(str(url), str(self.request.GET['next']))

        return url

    def get(self, request, *args, **kwargs):
        if (
            'proloauth_state' not in request.session
            or request.GET['state'] != request.session['proloauth_state']
        ):
            return super().get(request, *args, **kwargs)

        res = requests.post(
            '{}/token'.format(settings.OAUTH_ENDPOINT),
            json={
                'code': request.GET['code'],
                'client_id': settings.OAUTH_CLIENT_ID,
                'client_secret': settings.OAUTH_SECRET,
            },
        )
        handle_proloauth_response(request, res)
        return super().get(request, *args, **kwargs)
