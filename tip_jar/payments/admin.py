from django.apps import apps
from django.contrib import admin


@admin.register(apps.get_model("payments.Payment"))
class PaymentAdmin(admin.ModelAdmin):
    pass
