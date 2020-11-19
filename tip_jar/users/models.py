from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from unique_upload import unique_upload


def upload_to_users_user_profile_img(*args, **kwargs):
    return (
        f"django-storage/users/users/profile-imgs/" f"{unique_upload(*args, **kwargs)}"
    )


class User(AbstractUser):
    """Default user for Musician Tips."""

    profile_img = models.FileField(
        upload_to=upload_to_users_user_profile_img, null=True, blank=True
    )

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(max_length=280)

    venmo_url = models.URLField(max_length=200, blank=True, null=True)
    cash_app_url = models.URLField(max_length=200, blank=True, null=True)
    paypal_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
