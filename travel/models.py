from django.db import models
from django.conf import settings

class CompanionRequest(models.Model):
    info = models.TextField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companion')

    


class Trip(models.Model):
    description = models.TextField()
    number_of_seats = models.IntegerField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='triper', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now=True)


