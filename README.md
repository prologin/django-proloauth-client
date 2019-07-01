Django ProlOAuth
================

[![Build Status](https://travis-ci.com/prologin/django-proloauth.svg?branch=master)](https://travis-ci.com/prologin/django-proloauth)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Implementation of a minimalist OAuth client to login with a
[Prologin](https://github.com/prologin/site) account.


Requirements
------------

The library aims at being compatible with `python>=2.7` and django 2.


Installation
------------

```bash
pip install "git+https://github.com/prologin/django-proloauth"
```


Usage
-----

#### Setup

First, add **django_proloauth** to `INSTALLED_APPS`:

```python3
# settings.py

INSTALLED_APPS = (
    ...
    'django_proloauth',
)
```

You'll also need to apply migrations:

```bash
python3 manage.py migrate
```

Then, register `RefreshTokenMiddleware` in your middlewares, if you are using
Django's CSRF middleware, it is important that it gets to loaded after:

```python3
# settings.py

MIDDLEWARE = (
    ...
    'proloauth_client.middleware.RefreshTokenMiddleware',

    # Needs to be loaded after proloauth_client
    'django.middleware.csrf.CsrfViewMiddleware',
)
```

Finally, you need to include urls from the library:

```python3
# main_app/urls.py

urlpatterns = [
    ...

    # OAuth client
    path('user/auth/',
         include('proloauth_client.urls', namespace='proloauth_client')),
]
```

#### Connections

Once you completed the above setup, connecting through a Prologin account
should be as simple as following the url `proloauth_client:autologin`:

```html
<a href="{% url 'proloauth_client:autologin' %}">
    Sign in with my Prologin account
</a>
```


Deployment of your application
------------------------------

In order to allow connections to the main website, you need to specify the urls
of both API endpoints and setup a shared secret, for example the production
settings for should be as follows:

```python3
# settings.py on your app

OAUTH_ENDPOINT = 'https://prologin.org/user/auth'
OAUTH_SECRET = 'SECRET'
```

```python3
# settings/prod.py on Prologin's website

AUTH_TOKEN_CLIENTS = {
    'myapp': AuthTokenClient('SECRET', '//mywebsite.net/user/auth/callback'),
}
```


Protocol specifications
-----------------------

The protocol is detailed in the
[provider's sources](https://github.com/prologin/site/blob/master/prologin/users/auth_token_views.py).


Contributing
------------

#### Formatting

All of the python codebase needs to be formatted using [black](https://github.com/python/black)
by running `black .` at the root of the project before any commit.

You can automate the process by installing the recommended pre-commit hooks:

```bash
pip install -r requirements-dev.txt
pre-commit install
```
