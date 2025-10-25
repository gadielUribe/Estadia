from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='planta_inicio'),
    path('create/', views.crear, name='planta_crear'),
    path('<int:id_arbol>/edit/', views.editar, name='planta_editar'),
    path('<int:id_arbol>/delete/', views.eliminar, name='planta_eliminar')
]

