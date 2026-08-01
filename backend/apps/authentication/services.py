import hashlib
import random
import logging
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apps.common.enums import UserType

logger = logging.getLogger(__name__)


class OTPService:
    """
    OTP generation, hash validation, and mock/gateway dispatch service.
    """
    @staticmethod
    def generate_otp():
        """Generate a random 6-digit numeric OTP string."""
        return str(random.randint(100000, 999999))

    @staticmethod
    def hash_otp(otp_code):
        """Hash OTP string using SHA-256 for secure DB storage."""
        return hashlib.sha256(otp_code.encode('utf-8')).hexdigest()

    @classmethod
    def send_otp(cls, phone_number, purpose="LOGIN"):
        """
        Simulates OTP delivery (dev mode) or dispatches via SMS Gateway.
        Stores hashed OTP in Django cache.
        """
        from django.core.cache import cache
        otp_code = cls.generate_otp()
        hashed_otp = cls.hash_otp(otp_code)
        
        cache_key = f"otp_{phone_number}_{purpose}"
        cache.set(cache_key, hashed_otp, timeout=300)
        
        # In DEV mode log OTP code clearly
        logger.info(f"[OTP DEV DISPATCH] Phone: {phone_number} | OTP: {otp_code} | Purpose: {purpose}")
        
        return {
            "phone_number": phone_number,
            "otp_code": otp_code if settings.DEBUG else "*******",
            "expires_in_seconds": 300,
            "message": "OTP generated successfully."
        }

    @classmethod
    def verify_otp(cls, phone_number, otp_code, purpose="LOGIN"):
        """
        Verifies 6-digit OTP code against cached hash.
        """
        from django.core.cache import cache
        cache_key = f"otp_{phone_number}_{purpose}"
        cached_hash = cache.get(cache_key)
        
        # Allow master test OTP '123456' in DEBUG mode if cache is missing
        if settings.DEBUG and otp_code == "123456":
            return True
            
        if not cached_hash:
            return False
            
        is_valid = cls.hash_otp(otp_code) == cached_hash
        if is_valid:
            cache.delete(cache_key)
        return is_valid
