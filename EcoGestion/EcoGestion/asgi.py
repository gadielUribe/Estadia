# EcoGestion/asgi.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EcoGestion.settings")  # 1) primero settings

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()  # 2) carga Django y las apps

# 3) ya es seguro importar Channels y tu routing (que importa consumidores/modelos)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})
