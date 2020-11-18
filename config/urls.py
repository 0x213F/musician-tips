from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from .views import (
    MusicianCartView,
    MusicianDonateView,
    MusicianChooseView,
    MusicianCheckoutView,
    MusicianReceiptView,
)

urlpatterns = [
    # Static
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # API
    path("api/payments/", include("tip_jar.payments.urls", namespace="payments")),
    path("api/communications/", include("tip_jar.communications.urls", namespace="communications")),
    # Application
    path("<str:musician>/", MusicianChooseView.as_view(), name="donate"),
    path("<str:musician>/cart/", MusicianCartView.as_view(), name="cart"),
    path(
        "<str:musician>/choose/", MusicianDonateView.as_view(), name="choose"
    ),
    path(
        "<str:musician>/checkout/", MusicianCheckoutView.as_view(), name="checkout"
    ),
    path(
        "<str:musician>/receipt/", MusicianReceiptView.as_view(), name="receipt"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
