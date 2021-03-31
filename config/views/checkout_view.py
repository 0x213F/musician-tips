import stripe
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from config import utils as config_utils
from tip_jar.core.base_view import BaseView


User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY


class MusicianCheckoutView(BaseView):
    def get(self, request, musician, **kwargs):
        """
        By now the user has finalized their cart selection.

          - musician_amount: initial amount pledge.
          - transaction_covered: opt in to covering the transaction fees.
          - total_amount: the final total bill.
          - transaction_fee: how much goes to Stripe
          - website_amount: how much goes to the Musician Tips Dividend.
          - intent: mandatory setup for a Stripe transaction.
        """
        user = User.objects.get(username=musician)

        musician_amount = request.GET.get("amount")
        transaction_covered = request.GET.get("transactionCovered", False) == "true"

        (
            total_amount,
            musician_amount,
            transaction_fee,
        ) = config_utils.get_checkout_total(
            musician_amount,
            transaction_covered,
        )

        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * Decimal("100")),
            currency="usd",
            metadata={"musician": musician},
        )

        return self.template_response(
            request,
            "pages/checkout.html",
            {
                "client_secret": intent["client_secret"],
                "musician": user,
                "total_amount": total_amount,
                "musician_amount": musician_amount,
                "transaction_fee": transaction_fee,
                "transaction_covered": transaction_covered,
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            },
        )
