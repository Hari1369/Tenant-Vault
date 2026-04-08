import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    print(f"[DEBUG OTP] Email: {email} | OTP: {otp}")
    
    subject = "Your OTP Code"
    message = f"Your OTP is: {otp}"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )