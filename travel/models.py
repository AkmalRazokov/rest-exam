from django.db import models
from django.conf import settings


class Trip(models.Model):
    route = models.CharField(max_length=255)      
    date = models.DateField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route} on {self.date}"


class CompanionRequest(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='companions')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companion_requests', verbose_name='Пользователь')
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Request by {self.customer} for trip {self.trip}"
    

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.email} to {self.receiver.email} at {self.sent_at}"

