from django.urls import re_path

from apps.core.consumers import HMSConsumer

websocket_urlpatterns = [
    re_path(r'^ws/hms/$', HMSConsumer.as_asgi()),
]
