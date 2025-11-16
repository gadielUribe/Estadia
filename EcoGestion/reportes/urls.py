from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes_inicio, name='reportes_inicio'),
    path('especies/', views.reporte_especies, name='reporte_especies'),
    path('mantenimiento/', views.reporte_mantenimiento, name='reporte_mantenimiento'),
    path('tareas/', views.reportes_cumplimiento_usuarios, name='reporte_tareas'),
    path('actividades_usuario/', views.reporte_actividades_usuario, name='reporte_actividades'),
    path('uso_herramientas/', views.reporte_uso_herramientas, name='reporte_uso_herramientas'),
    path('productos_inventario/', views.reporte_productos_inventario, name='reporte_productos_inventario'),
]
