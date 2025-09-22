import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatGeneral, ChatPrivado

class GeneralChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_general'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje = data['mensaje']
        usuario_id = self.scope['user'].id_usuario
        usuario_nombre = self.scope['user'].nombre_completo

        await self.save_message(usuario_id, mensaje)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensaje': mensaje,
                'usuario_nombre': usuario_nombre,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'mensaje': event['mensaje'],
            'usuario_nombre': event['usuario_nombre'],
        }))

    @database_sync_to_async
    def save_message(self, usuario_id, mensaje):
        ChatGeneral.objects.create(usuario_id=usuario_id, mensaje=mensaje)

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.receptor_id = self.scope['url_route']['kwargs']['receptor_id']
        self.room_name = f'privado_{min(self.user.id_usuario, int(self.receptor_id))}_{max(self.user.id_usuario, int(self.receptor_id))}'
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje = data['mensaje']
        await self.save_message(self.user.id_usuario, self.receptor_id, mensaje)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensaje': mensaje,
                'emisor_nombre': self.user.nombre_completo,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'mensaje': event['mensaje'],
            'emisor_nombre': event['emisor_nombre'],
        }))

    @database_sync_to_async
    def save_message(self, emisor_id, receptor_id, mensaje):
        ChatPrivado.objects.create(emisor_id=emisor_id, receptor_id=receptor_id, mensaje=mensaje)