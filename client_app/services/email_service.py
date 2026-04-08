from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email, otp):
    print(f"[DEBUG OTP]: {otp}")

    send_mail(
        "Your OTP Code",
        f"Your OTP is {otp}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )