import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

import chat_bot.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codefest.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
"websocket": AuthMiddlewareStack(
        URLRouter(
            chat_bot.routing.websocket_urlpatterns
        )
    ),
  # Just HTTP for now. (We can add other protocols later.)
})
