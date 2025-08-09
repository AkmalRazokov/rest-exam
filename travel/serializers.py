from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Trip, CompanionRequest, Message
from rest_framework import serializers

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class CompanionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanionRequest
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'sent_at', 'read']
        read_only_fields = ['sent_at', 'read']


