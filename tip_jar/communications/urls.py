from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from tip_jar.communications.views import (
    SubscriptionCreateView
)


app_name = "communications"
urlpatterns = [
    path(
        "subscription/create/",
        view=SubscriptionCreateView.as_view(),
        name="subscription-create"
    ),
]
