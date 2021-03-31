import decimal
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from config import utils as config_utils
from tip_jar.core.base_view import BaseView

User = get_user_model()


class MusicianCartView(BaseView):
    def get(self, request, musician, **kwargs):
        """
        After the user has selected a donation amount, show them the cart view.

          - musician_amount: initial amount pledge.
          - transaction_covered: opt in to covering the transaction fees.
          - total_amount: the final total bill.
          - transaction_fee: how much goes to Stripe.
          - website_amount: how much goes to the Musician Tips Dividend.
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

        return self.template_response(
            request,
            "pages/cart.html",
            {
                "musician": user,
                "total_amount": total_amount,
                "musician_amount": musician_amount,
                "transaction_fee": transaction_fee,
                "transaction_covered": transaction_covered,
                "website_donation_amount": settings.WEBSITE_DONATION_AMOUNT,
            },
        )
