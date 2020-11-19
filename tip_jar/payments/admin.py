from django.apps import apps
from django.contrib import admin


@admin.register(apps.get_model("payments", "Payment"))
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(apps.get_model("payments", "AmountChoice"))
class AmountChoiceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        AmountChoice = apps.get_model("payments", "AmountChoice")
        qs = AmountChoice.objects.all()
        qs = qs.order_by("amount")
        return qs
