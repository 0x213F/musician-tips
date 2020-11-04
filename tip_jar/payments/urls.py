from django.urls import path

from tip_jar.payments.views import (
    CreateStripePaymentView,
)


app_name = "payments"
urlpatterns = [
    path(
        "stripe/create-intent",
        view=CreateStripePaymentView.as_view(),
        name="redirect"
    ),
]
