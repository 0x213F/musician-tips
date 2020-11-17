import decimal
import stripe
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from tip_jar.core.base_view import BaseView

User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY


def get_transaction_fee(total_amount):
    return ((total_amount) * Decimal('0.029') + Decimal('0.3')).quantize(Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)


class MusicianCheckoutView(BaseView):

    def get(self, request, musician, **kwargs):
        """
        Load musician homepage.
        """
        user = User.objects.get(username=musician)

        musician_amount = request.GET.get('amount')
        website_donation = request.GET.get('websiteDonation', False) == 'true'
        transaction_covered = request.GET.get('transactionCovered', False) == 'true'

        if website_donation:
            website_amount = Decimal('0.25')
        else:
            website_amount = Decimal('0.00')


        musician_amount = Decimal(musician_amount) / Decimal('100')

        if transaction_covered:
            total_amount = musician_amount + website_amount
            proposed_total = total_amount
            while True:
                proposed_total += Decimal('0.01')
                proposed_transaction_fee = proposed_total - total_amount
                actual_transaction_fee = get_transaction_fee(proposed_total)
                if actual_transaction_fee <= proposed_transaction_fee:
                    break
            transaction_fee = get_transaction_fee(proposed_total)
            musician_amount = proposed_total - website_amount - transaction_fee

        else:
            transaction_fee = get_transaction_fee(musician_amount + website_amount)
            musician_amount -= transaction_fee

        total_amount = musician_amount + website_amount + transaction_fee

        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * Decimal('100')),
            currency="usd",
            metadata={'musician': musician},
        )

        return self.template_response(request, "pages/checkout.html", {
            "client_secret": intent["client_secret"],
            "musician": user,
            "total_amount": total_amount,
            "musician_amount": musician_amount,
            "transaction_fee": transaction_fee,
            "transaction_covered": transaction_covered,
            "website_amount": website_amount,
            "website_donation": website_donation,
        })
