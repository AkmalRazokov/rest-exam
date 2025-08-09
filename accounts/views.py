from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import CustomUserSerializer
from .helpers import send_confirmation_token
from .models import ConfirmationToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()


@api_view(["POST"])
def user_register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    password1 = request.data.get('password1')
    if not email or not password or not password1:
        return Response({'error': 'Email, password and password1 are required'}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response({'message': 'User registered successfully. Confirmation email sent.'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'User created, but confirmation email was not sent.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username = email, password = password)
    if user is not None:
        if user.is_confirmed_email:
            login(request, user)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email not confirmed'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def user_logout(request):
    try:
        logout(request)
        return Response('logout')
    except Exception as ex:
        return Response({'error':str(ex)})
    


@api_view(['GET'])
def confirm_email(request, token):
    try:
        email_confirm_object = ConfirmationToken.objects.get(token=token)
    except ConfirmationToken.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    user = email_confirm_object.user
    user.is_active = True
    user.is_confirmed_email = True
    user.save()
    email_confirm_object.delete()
    return Response({'message': 'Email confirmed successfully.'}, status=status.HTTP_200_OK)
    



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request):
    user = request.user
    if request.method == "GET":
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CustomUserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PATCH":
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'Аккаунт удалён'}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({"errors":'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(email=email)
    ConfirmationToken.objects.filter(user = user).delete()
    token_obj = ConfirmationToken.objects.create(user = user)
    reset_link = f"http://127.0.0.1:8000/auth/reset-password-confirm/{token_obj.token}/"
    send_mail(
            subject="Сброс пароля",
            message=f"Для сброса пароля перейдите по ссылке: {reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
    return Response({'message': 'Password reset email sent'})



@api_view(['POST'])
def confirm_password_reset(request, token):
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')
    if not password or not password_confirm:
        return Response({'error':'Both password fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    if password != password_confirm:
        return Response({'error':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    token_obj = ConfirmationToken.objects.get(token=token)
    if not token_obj:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    if token_obj.is_expired():
        token_obj.delete()
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    user = token_obj.user
    user.set_password(password)
    user.save()
    token_obj.delete()
    return Response({"message":'Password successfully reset'})
