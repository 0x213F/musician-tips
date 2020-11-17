import json
import os
import stripe

from django.conf import settings

from tip_jar.core.base_view import BaseView

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
