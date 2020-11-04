import json
import os
import stripe

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from tip_jar.core.base_view import BaseView
from tip_jar import secrets

User = get_user_model()
stripe.api_key = secrets.STRIPE_API_KEY



class CreateStripePaymentView(BaseView):

    def post(self, request, **kwargs):
        """
        Accept payment from Stripe
        """
        data = json.loads(request.body.decode("utf-8"))
        amount = data["amount"]
        if not amount:
            raise ValueError("You must include the payment amount.")

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
        )
        return self.http_response_200({
            "clientSecret": intent["client_secret"]
        })
