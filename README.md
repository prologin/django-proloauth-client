Django OAuth
============

Implementation of a minimalist OAuth client to login with a
[Prologin](https://github.com/prologin/site) account.


Requirements
------------

The library aims at beeing compatible with `python>=2.7` and django 2.
Specific requirements are listed in requirements.txt.


Installation
------------

```bash
# Add the dependancy to requirements.txt
( echo "# Prologin's Django OAuth" ;
  echo "git+https://github.com/prologin/django-oauth" ) >> requirements.txt

# Update your dependancies, preferably in a virtual env
pip install -U -r requirements.txt
```


Usage
-----

#### Setup

First, add **django_oauth** to `INSTALLED_APPS`:

```python3
# settings.py

INSTALLED_APPS = (
    ...
    'django_oauth',
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
    'oauth_client.middleware.RefreshTokenMiddleware',

    # Needs to be loaded after oauth_client
    'django.middleware.csrf.CsrfViewMiddleware',
)
```

Finally, you need to include urls from the library:

```python3
# main_app/urls.py

urlpatterns = [
    ...

    # OAuth client
    path('user/auth/', include('oauth_client.urls', namespace='oauth_client')),
]
```

#### Connections

Once you completed the above setup, connecting through a Prologin account
should be as simple as following the url `oauth_client:autologin`:

```html
<a href="{% url 'oauth_client:autologin' %}">
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
