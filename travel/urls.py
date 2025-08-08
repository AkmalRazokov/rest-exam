from django.urls import path
from .views import *

urlpatterns = [
    path('trip', trip_list_create),
    path('trip/<int:pk>', list_detail_update_delete),
]