from django.db import models
from django.conf import settings

class ChatGeneral(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ChatGeneral'

class ChatPrivado(models.Model):
    id_chat = models.AutoField(primary_key=True)
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_recibidos', on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ChatPrivado'