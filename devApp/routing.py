from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/dady/$',consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/socket-server/Notification/$',consumers.ChatConsumer.as_asgi()),
]