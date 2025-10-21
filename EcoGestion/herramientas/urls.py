from django.urls import path
from . import views

app_name = 'herramientas'

urlpatterns = [
    # Herramientas CRUD
    path('', views.herramienta_list, name='herramienta_list'),
    path('nueva/', views.herramienta_create, name='herramienta_create'),
    path('editar/<int:pk>/', views.herramienta_update, name='herramienta_update'),
    path('eliminar/<int:pk>/', views.herramienta_delete, name='herramienta_delete'),

    # Asignaciones
    path('asignaciones/', views.asignacion_list, name='asignacion_list'),
    path('asignar/', views.asignar_herramienta, name='asignar_herramienta'),
    path('asignaciones/eliminar/<int:pk>/', views.asignacion_delete, name='asignacion_delete'),
]
