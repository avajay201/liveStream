from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'stream/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'stream/live/(?P<stream_key>[^/]+)/$', consumers.StreamConsumer.as_asgi()),
]
