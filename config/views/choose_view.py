from django.apps import apps
from django.contrib.auth import get_user_model

from tip_jar.core.base_view import BaseView

User = get_user_model()


class MusicianChooseView(BaseView):
    def get(self, request, musician, **kwargs):
        """
        Load a musician's homepage. It displays custom amount choices that the
        musician has set up.
        """
        AmountChoice = apps.get_model("payments", "AmountChoice")

        user = User.objects.get(username=musician)
        amount_choices = (
            AmountChoice.objects.filter(user=user)
            .order_by("amount")
            .values_list("amount", flat=True)
        )

        return self.template_response(
            request,
            "pages/choose.html",
            {
                "musician": user,
                "amount_choices": amount_choices,
            },
        )
