from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'stream/live/(?P<stream_key>[^/]+)/(?P<user>[^/]+)/$', consumers.StreamConsumer.as_asgi()),
]
