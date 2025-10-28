from django.db import models
from django.conf import settings

class BackupAudit(models.Model):
    ACTIONS = [
        ('BACKUP', 'Backup generado'),
        ('RESTORE', 'Restauración aplicada'),
        ('UPLOAD', 'Respaldo subido'),
        ('DOWNLOAD', 'Respaldo descargado'),
    ]
    action = models.CharField(max_length=10, choices=ACTIONS)
    filename = models.CharField(max_length=255)  # p.ej. EcoGest_2025-10-27_18-20-05.sql
    run_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    log = models.TextField(blank=True, default='')  # stdout/stderr del proceso, mensajes, etc.

    class Meta:
        ordering = ['-run_at']

    def __str__(self):
        return f'{self.action} - {self.filename} - {self.run_at:%Y-%m-%d %H:%M}'
