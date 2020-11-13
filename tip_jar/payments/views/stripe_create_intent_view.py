import json
import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from tip_jar.core.base_view import BaseView

User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY



class StripeCreateIntentView(BaseView):

    def post(self, request, **kwargs):
        """
        Accept payment from Stripe
        """

        data = json.loads(request.body.decode("utf-8"))
        amount = data["amount"]
        musician = data["musician"]

        if not amount:
            raise ValueError("You must include the payment amount.")

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            metadata={'musician': musician},
        )
        return self.http_response_200({
            "clientSecret": intent["client_secret"]
        })
