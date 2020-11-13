import json
import os
import stripe
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from tip_jar.core.base_view import BaseView

User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY



class GetRecentlyPaidUsersView(BaseView):

    def get(self, request, **kwargs):
        """
        Accept payment from Stripe
        """
        Payment = apps.get_model('payments', 'Payment')

        one_hour_ago = timezone.now() - timedelta(hours=1)
        recently_payments = (
            Payment.objects
            .filter(user__isnull=False, created_at__gte=one_hour_ago)
            .order_by("created_at")
        )

        recently_paid_users = set()
        for payment in recently_payments:
            recently_paid_users.add(payment.user_id)
        return self.http_response_200({
            "recentlyPaidUsers": list(recently_paid_users),
        })
