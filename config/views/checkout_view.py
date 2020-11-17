import decimal
import stripe
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from tip_jar.core.base_view import BaseView

User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY


class MusicianCheckoutView(BaseView):

    def get(self, request, musician, **kwargs):
        """
        Load musician homepage.
        """
        user = User.objects.get(username=musician)

        total_amount = request.GET.get('total')
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency="usd",
            metadata={'musician': musician},
        )

        total_amount = (Decimal(total_amount) / Decimal('100')).quantize(Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)

        return self.template_response(request, "pages/checkout.html", {
            "musician": user,
            "client_secret": intent["client_secret"],
            "total_amount": total_amount,
        })
