import pgtrigger
import uuid

from django.db import models


@pgtrigger.register(
    pgtrigger.Protect(
        name="protect_update",
        operation=(pgtrigger.Update),
    )
)
class Subscription(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "email"]

    def __str__(self):
        return f"[{self.user}] {self.email}"
