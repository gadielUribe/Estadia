from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='incidencia_inicio'),
    path('create/', views.crear, name='crear_incidencia'),
    path('<int:id_incidencia>/edit/', views.editar, name='editar_incidencia'),
    path('<int:id_incidencia>/delete/', views.eliminar, name='eliminar_incidencia')
]
