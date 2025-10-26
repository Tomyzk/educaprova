import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ComplexityPasswordValidator:
    message = "A senha deve conter ao menos 1 letra maiúscula e 1 número."

    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password or ""):
            raise ValidationError(self.message)
        if not re.search(r"\d", password or ""):
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message

