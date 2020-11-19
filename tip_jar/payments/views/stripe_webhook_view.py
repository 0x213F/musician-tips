import json
import stripe

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from tip_jar.core.base_view import BaseView

User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY


class StripeWebhookView(BaseView):
    def post(self, request, **kwargs):
        """"""
        Payment = apps.get_model("payments", "Payment")

        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        # print(request.body)

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            return self.http_response_400("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            return self.http_response_400("Invalid signature")

        if event.type != "payment_intent.succeeded":
            return self.http_response_400(f"Unhandled event type {event.type}")

        amount = event.data.object["amount"]
        try:
            username = event.data.object["metadata"]["musician"]
            # print(event.data.object)
            user = User.objects.get(username=username)
        except (KeyError, User.DoesNotExist):
            user = None

        payment = Payment.objects.create(
            user=user,
            amount=amount,
        )

        return self.http_response_200({})
