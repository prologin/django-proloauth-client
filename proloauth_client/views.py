# Copyright (C) <2019> Association Prologin <association@prologin.org>
# SPDX-License-Identifier: GPL-3.0+

import requests
from urllib.parse import urlencode

from django.conf import settings
from django.views.generic import RedirectView

from proloauth_client.utils import handle_proloauth_response, gen_auth_state


class AutoLogin(RedirectView):
    def get_redirect_url(self):
        self.request.session['proloauth_state'] = gen_auth_state()
        return '{}/authorize?{}'.format(
            settings.OAUTH_ENDPOINT,
            urlencode(
                {
                    'client_id': settings.OAUTH_CLIENT_ID,
                    'state': self.request.session['proloauth_state'],
                }
            ),
        )


class Callback(RedirectView):
    def get_redirect_url(self):
        return settings.LOGIN_REDIRECT_URL

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
