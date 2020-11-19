from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from tip_jar.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = tuple(auth_admin.UserAdmin.fieldsets) + (
        (
            "Payment Options",
            {
                "fields": (
                    "venmo_url",
                    "cash_app_url",
                    "paypal_url",
                )
            },
        ),
        (
            "Display",
            {
                "fields": (
                    "name",
                )
            },
        ),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
