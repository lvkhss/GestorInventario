from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length)
        self.message = 'La contraseña es demasiado corta. Debe tener al menos %(min_length)d caracteres.'

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                self.message % {'min_length': self.min_length},
                code='password_too_short',
            )

    def get_help_text(self):
        return 'La contraseña debe tener al menos %d caracteres.' % self.min_length
