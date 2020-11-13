from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from unique_upload import unique_upload


def upload_to_comments_voice_recordings(*args, **kwargs):
    return (
        f"django-storage/comments/voice-recordings/audios/"
        f"{unique_upload(*args, **kwargs)}"
    )


class User(AbstractUser):
    """Default user for Tip Jar."""

    name = models.CharField(max_length=280)

    profile_img = models.FileField(upload_to=upload_to_comments_voice_recordings, null=True, blank=True)

    #: First and last name do not cover name patterns around the globe
    landing_text = models.CharField(default="Thank you for listening. Gracias por su atención.", blank=True, max_length=140)

    venmo_url = models.URLField(max_length=200, blank=True, null=True)
    cash_app_url = models.URLField(max_length=200, blank=True, null=True)
    paypal_url = models.URLField(max_length=200, blank=True, null=True)
    has_stripe_enabled = models.BooleanField(default=False, blank=True)
