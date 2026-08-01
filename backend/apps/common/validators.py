import re
from django.core.exceptions import ValidationError


def validate_indian_phone_number(value):
    """
    Validates that a phone number is a valid 10-digit Indian mobile number
    starting with 6, 7, 8, or 9.
    """
    if not value:
        raise ValidationError("Phone number is required.")
    
    pattern = r'^[6-9]\d{9}$'
    if not re.match(pattern, str(value)):
        raise ValidationError(
            "Enter a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9."
        )
