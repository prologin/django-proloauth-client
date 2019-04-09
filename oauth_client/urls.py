from django.urls import path

from oauth_client import views


app_name = 'oauth_client'

urlpatterns = [
    path('autologin/', views.AutoLogin.as_view(), name='autologin'),
    path('callback/', views.Callback.as_view(), name='auth_callback'),
]
