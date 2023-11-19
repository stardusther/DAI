from django.core.exceptions import ValidationError


def validate_capitalized(value):
    """Validate that the first letter of the value is capitalized"""
    if value[0].islower():
        raise ValidationError('Value must be capitalized')
