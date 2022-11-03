from django.core.exceptions import ValidationError


def validate_length(value):
    length = len(str(value))
    if length!=10:
        raise ValidationError(
            "Number you entered is not valid."
        )