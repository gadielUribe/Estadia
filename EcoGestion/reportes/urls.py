from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes_inicio, name='reportes_inicio'),
    path('especies/', views.reporte_especies, name='reporte_especies'),
    path('mantenimiento/', views.reporte_mantenimiento, name='reporte_mantenimiento'),
    path('tareas/', views.reportes_cumplimiento_usuarios, name='reporte_tareas'),
    path('actividades_usuario/', views.reporte_actividades_usuario, name='reporte_actividades'),
]
