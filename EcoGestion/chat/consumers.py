import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from .models import ChatGeneral, ChatPrivado 

def serialize_general(m):
    return {
        "id": m.id_mensaje,
        "mensaje": m.mensaje,
        "usuario_nombre": getattr(m.usuario, "nombre_completo", str(m.usuario)),
        "timestamp": m.fecha_envio.isoformat(),
    }

def serialize_privado(m):
    return {
        "id": m.id_chat,
        "mensaje": m.mensaje,
        "emisor_id": m.emisor_id,
        "emisor_nombre": getattr(m.emisor, "nombre_completo", str(m.emisor)),
        "receptor_id": m.receptor_id,
        "timestamp": m.fecha_envio.isoformat(),
    }

class GeneralChatConsumer(AsyncWebsocketConsumer):
    room_group_name = "chat_general"

    async def connect(self):
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Enviar los últimos N mensajes como historial inicial
        ultimos = await self.get_last_messages(limit=50)
        await self.send(text_data=json.dumps({"type": "history", "messages": ultimos}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            await self.send(text_data=json.dumps({"type": "error", "detail": "auth_required"}))
            return

        data = json.loads(text_data)
        mensaje = (data.get("mensaje") or "").strip()
        if not mensaje:
            return

        # Guarda y retransmite
        msg = await self.save_message(user, mensaje)
        payload = serialize_general(msg)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "payload": payload}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "message", **event["payload"]}))

    @database_sync_to_async
    def get_last_messages(self, limit=50):
        qs = (ChatGeneral.objects
              .select_related("usuario")
              .order_by("-fecha_envio", "-id_mensaje")[:limit])
        # los devolvemos en orden cronológico ascendente
        return [serialize_general(m) for m in reversed(list(qs))]

    @database_sync_to_async
    def save_message(self, user, texto):
        return ChatGeneral.objects.create(usuario=user, mensaje=texto)

class PrivateChatConsumer(AsyncWebsocketConsumer):
    """
    Canal privado entre self.scope['user'] y receptor_id (URL).
    Historial al conectar y broadcast en el grupo único de la pareja.
    """
    async def connect(self):
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        # Usa siempre la PK del usuario (alias a id_usuario en tu modelo)
        self.emisor_id = int(getattr(user, "id_usuario", user.pk))
        self.receptor_id = int(self.scope["url_route"]["kwargs"]["receptor_id"])

        # Evitar conectar a un chat consigo mismo
        if self.emisor_id == self.receptor_id:
            await self.close()
            return

        # Nombre de grupo simétrico (igual para ambos usuarios)
        a, b = sorted([self.emisor_id, self.receptor_id])
        self.room_group_name = f"chat_priv_{a}_{b}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Historial inicial
        ultimos = await self.get_last_messages(self.emisor_id, self.receptor_id, limit=50)
        await self.send(text_data=json.dumps({"type": "history", "messages": ultimos}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            await self.send(text_data=json.dumps({"type": "error", "detail": "auth_required"}))
            return

        data = json.loads(text_data)
        mensaje = (data.get("mensaje") or "").strip()
        if not mensaje:
            return

        emisor_nombre = getattr(user, "nombre_completo", str(user))
        msg_id, fecha = await self.save_message(self.emisor_id, self.receptor_id, mensaje)
        payload = {
            "id": msg_id,
            "mensaje": mensaje,
            "emisor_id": self.emisor_id,
            "emisor_nombre": emisor_nombre,
            "receptor_id": self.receptor_id,
            "timestamp": fecha.isoformat(),
        }
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "payload": payload})

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "message", **event["payload"]}))

    # -------- DB helpers --------
    @database_sync_to_async
    def get_last_messages(self, uid, rid, limit=50):
        qs = (ChatPrivado.objects
              .filter(Q(emisor_id=uid, receptor_id=rid) | Q(emisor_id=rid, receptor_id=uid))
              .select_related("emisor")
              .order_by("-fecha_envio")[:limit])
        return [serialize_privado(m) for m in reversed(list(qs))]

    @database_sync_to_async
    def save_message(self, uid, rid, texto):
        obj = ChatPrivado.objects.create(emisor_id=uid, receptor_id=rid, mensaje=texto)
        return obj.id_chat, obj.fecha_envio
