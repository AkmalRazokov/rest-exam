from django.urls import path
from .views import *

urlpatterns = [
    path('trip/', trip_list_create),
    path('trip/<int:pk>', trip_detail_update_delete),

    path('companion/', list_create_companion_request),
    path('message/', messages_list_create),
    path('companion/<int:pk>/', companion_request_detail),

]