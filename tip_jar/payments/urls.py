from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from tip_jar.payments.views import (
    StripeWebhookView,
)


app_name = "payments"
urlpatterns = [
    path(
        "stripe/webhook/",
        view=csrf_exempt(StripeWebhookView.as_view()),
        name="redirect"
    ),
]
