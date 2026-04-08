import random
import time
from django.core.cache import cache

OTP_EXPIRY = 300        # 5 minutes
OTP_COOLDOWN = 60       # 1 minute


def generate_otp():
    otp = random.randint(100000, 999999)
    otp_str = str(otp)
    return otp_str


def set_otp(identifier, otp):
    cache.set("otp_" + identifier, otp, timeout=OTP_EXPIRY)
    current_time = time.time()
    cache.set("otp_time_" + identifier, current_time, timeout=OTP_EXPIRY)


def get_otp(identifier):
    otp = cache.get("otp_" + identifier)
    return otp


def is_otp_expired(identifier):
    otp_time = cache.get("otp_time_" + identifier)

    if otp_time is None:
        return True

    current_time = time.time()
    time_difference = current_time - otp_time

    if time_difference > OTP_EXPIRY:
        return True
    else:
        return False


def can_resend_otp(identifier):
    last_time = cache.get("otp_time_" + identifier)
    if last_time is None:
        return True

    current_time = time.time()
    time_difference = current_time - last_time
    if time_difference > OTP_COOLDOWN:
        return True
    else:
        return False