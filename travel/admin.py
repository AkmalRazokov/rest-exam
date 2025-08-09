from django.contrib import admin
from .models import Trip, CompanionRequest, Message

admin.site.register(Trip)
admin.site.register(CompanionRequest)
admin.site.register(Message)
