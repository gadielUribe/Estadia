from django.urls import path
from . import views

app_name = 'herramientas'

urlpatterns = [
    path('', views.herramienta_list, name='herramienta_list'),
    path('nueva/', views.herramienta_create, name='herramienta_create'),
    path('editar/<int:pk>/', views.herramienta_update, name='herramienta_update'),
    path('eliminar/<int:pk>/', views.herramienta_delete, name='herramienta_delete'),
    path('<int:pk>/tareas/', views.herramienta_tareas, name='herramienta_tareas'),
]
