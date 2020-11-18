import json

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from tip_jar.core.base_view import BaseView

User = get_user_model()


class SubscriptionCreateView(BaseView):
    def post(self, request, **kwargs):
        """
        """
        Subscription = apps.get_model('communications', 'Subscription')

        data = json.loads(request.body.decode("utf-8"))

        musician_username = data['musicianUsername']
        user = User.objects.get(username=musician_username)

        Subscription.objects.create(
            user=user,
            email=data['subscriptionEmail'],
        )

        return self.http_response_200({})
