from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from tip_jar.payments.views import (
    GetRecentlyPaidUsersView,
    StripeWebhookView,
)


app_name = "payments"
urlpatterns = [
    path(
        "get-recently-paid-users/",
        view=GetRecentlyPaidUsersView.as_view(),
        name="get-recently-paid-users",
    ),
    path(
        "stripe/webhook/",
        view=csrf_exempt(StripeWebhookView.as_view()),
        name="redirect"
    ),
]
