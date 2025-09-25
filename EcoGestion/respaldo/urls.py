from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_respaldos, name='respaldo_inicio'),
    path('backups/', views.backup_now, name="backup_now"),
    path('restore/latest/', views.restore_latest, name='restore_latest'),
    path('restore/<str:filename>/', views.restore_file, name='restore_file'),
    path('download/<str:filename>/', views.download_backup, name='download'),
    path('upload/', views.upload_backup, name='upload'),
]