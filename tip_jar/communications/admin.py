from django.apps import apps
from django.contrib import admin


@admin.register(apps.get_model("communications", "Subscription"))
class SubscriptionAdmin(admin.ModelAdmin):
    pass
