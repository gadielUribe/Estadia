from django.contrib import admin
from .models import BackupAudit

@admin.register(BackupAudit)
class BackupAuditAdmin(admin.ModelAdmin):
    list_display = ('action', 'filename', 'run_at', 'user')
    search_fields = ('filename', 'log')
    list_filter = ('action', 'run_at')
