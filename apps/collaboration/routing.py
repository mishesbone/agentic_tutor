from django.urls import re_path
from .consumers import CollabConsumer

websocket_urlpatterns = [
    re_path(r'ws/collaboration/(?P<room_name>\w+)/$', CollabConsumer.as_asgi()),
]
