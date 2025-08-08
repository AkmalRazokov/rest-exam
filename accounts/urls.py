from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_register),
    path('login/', user_login),
    path('logout/', user_logout),
]