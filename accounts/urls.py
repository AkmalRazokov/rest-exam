from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_register),
    path('login/', user_login),
    path('logout/', user_logout),
    path('user/', user_detail),

    path('confirm/<uuid:token>/', confirm_email),

    path('reset-password-request/', request_password_reset),
    path('reset-password-confirm/<uuid:token>/', confirm_password_reset, name='reset_password_confirm'),
]