from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Plan(models.TextChoices):
        FREE = "FREE", "Free"
        PREMIUM = "PREMIUM", "Premium"

    # Login por e-mail
    email = models.EmailField(unique=True)

    plan = models.CharField(
        max_length=16,
        choices=Plan.choices,
        default=Plan.FREE,
        help_text="Plano atual do usuário",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_guest = models.BooleanField(default=False)
    guest_expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.plan})"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
