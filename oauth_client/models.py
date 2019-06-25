# Copyright (C) <2019> Association Prologin <association@prologin.org>
# SPDX-License-Identifier: GPL-3.0+

from django.conf import settings
from django.db import models


class OAuthToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE
    )
    token = models.CharField(max_length=64, null=True, default=None)
