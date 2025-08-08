from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Trip
from .serializers import TripSerializer


@api_view(['GET', 'POST'])
def trip_list_create(request):
    if request.method == "GET":
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many = True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = TripSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'PATCH' 'DELETE'])
def list_detail_update_delete(request, pk):
        trip = Trip.objects.filter(id = pk).first()
        if trip is None:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == "GET":
            serializers = TripSerializer(trip)
            return Response(serializers.data)
        
        if request.method == "PUT":
            serializers = TripSerializer(trip, data = request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == "PATCH":
            serializer = TripSerializer(trip, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == "DELETE":
            try:
                trip.delete()
                return Response(status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({'errors':str(ex)})
       
        

        


