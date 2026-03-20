import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.collaboration.routing

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ASGI application
application = ProtocolTypeRouter({
    # HTTP requests go to standard Django ASGI app
    "http": get_asgi_application(),

    # WebSocket requests go through Channels AuthMiddleware and URLRouter
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.collaboration.routing.websocket_urlpatterns
        )
    ),
})
