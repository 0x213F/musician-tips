from django.contrib.auth import get_user_model

from tip_jar.core.base_view import BaseView

User = get_user_model()


class MusicianDonateView(BaseView):

    def get(self, request, musician, **kwargs):
        """
        Load musician homepage.
        """

        user = User.objects.get(username=musician)

        return self.template_response(request, "pages/donate.html", {
            "musician": user,
        })
