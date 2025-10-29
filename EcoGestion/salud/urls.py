# salud/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='salud_inicio'),
    path('create/', views.crear, name='salud_crear'),
    path('<int:id_registro>/edit/', views.editar, name='salud_editar'),
    path('<int:id_registro>/delete/', views.eliminar, name='salud_eliminar'),
    path('planta/<int:planta_id>/', views.historial_planta, name='salud_historial_planta'),
]
