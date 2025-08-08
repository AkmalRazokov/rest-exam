from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import CustomUserSerializer
from .helpers import send_confirmation_token
from .models import ConfirmationToken


@api_view(["POST"])
def user_register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    password1 = request.data.get('password1')
    if not email or not password or not password1:
        return Response('errors', status=status.HTTP_400_BAD_REQUEST)
    if password != password1:
        return Response({'error': 'check password.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email =email).exists():
        return Response({'error':'пользователь с таким email существует'},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(email=email, password=password)
    user.is_active = False
    user.save()
    confirm_email_object = ConfirmationToken.objects.create(user = user)
    token = confirm_email_object.token
    res = send_confirmation_token(email, token)
    if res["is_sent"]:
        return Response('Good')
    return Response({'message':'registered'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response('errors', status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, email = email, password = password)
    if user is not None:
        if user.is_confirmed_email:
            login(request, user)
            serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('errors')


@api_view(["GET"])
def user_logout(request):
    try:
        logout(request)
        return Response('logout')
    except Exception as ex:
        return Response({'error':str(ex)})
    



def confirm_email(request, token):
    try:
        email_confirm_object = ConfirmationToken.objects.get(token=token)
    except ConfirmationToken.DoesNotExist:
        Response('error')
    user = email_confirm_object.user
    user.is_active = True
    user.is_confirmed_email = True
    user.save()
    email_confirm_object.delete()
    return redirect("login")