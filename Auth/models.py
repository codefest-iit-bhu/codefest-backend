from django.db import models
from django.contrib.auth.models import User
from .utils import FirebaseAPI

# Create your models here.


class VerifiedAccount(models.Model):
    AUTH_FACEBOOK_PROVIDER = "facebook.com"
    AUTH_GOOGLE_PROVIDER = "google.com"
    AUTH_GITHUB_PROVIDER = "github.com"
    AUTH_EMAIL_PROVIDER = "password"

    AUTH_PROVIDERS_CHOICE = (
        (AUTH_FACEBOOK_PROVIDER, "Facebook"),
        (AUTH_GOOGLE_PROVIDER, "Google"),
        (AUTH_GITHUB_PROVIDER, "Github"),
        (AUTH_EMAIL_PROVIDER, "Email"),
    )

    uid = models.CharField(max_length=64, primary_key=True, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="verified_account",
        related_query_name="account",
    )
    provider = models.CharField(choices=AUTH_PROVIDERS_CHOICE, max_length=15)
    provider_uid = models.CharField(max_length=64, null=True, blank=True)
    is_verified = models.BooleanField(default=True)

    class Meta:
        unique_together = ("provider", "provider_uid")
        app_label = "Auth"

    def __str__(self):
        return f"{self.user} from {self.provider}"

    def get_verified_status(self):
        if self.is_verified:
            return True
        self.is_verified = FirebaseAPI.get_email_confirmation_status(self.uid)
        self.save()
        return self.is_verified
