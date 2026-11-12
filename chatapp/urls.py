from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path

from chatapp2.consumers import PrivateChatConsumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chatapp2.urls")),
    path("accounts/", include("accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

websocket_urlpatterns = [
    re_path(r"ws/chat/$", PrivateChatConsumer.as_asgi()),
]
