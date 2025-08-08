from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Trip

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'