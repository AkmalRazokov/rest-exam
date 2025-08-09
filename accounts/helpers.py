from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_token(email, token):
    path = f"http://127.0.0.1:8000/auth/confirm-email/{token}"
    message = f" click here {path} to confirm your email"
    from_email = settings.EMAIL_HOST_USER
    try:
        send_mail(subject="Welcome to project!",
                  message=message,
                  from_email=from_email,
                  recipient_list = [email])
        return {
            "is_sent": True,
            "message": "Message sended succesfully"
        }
    except Exception as e:
        return{
            "is_sent":False,
            "message":str(e)
        }
