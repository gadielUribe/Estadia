from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/general/$', consumers.GeneralChatConsumer.as_asgi()),
    re_path(r'ws/chat/privado/(?P<receptor_id>\d+)/$', consumers.PrivateChatConsumer.as_asgi()),
]
