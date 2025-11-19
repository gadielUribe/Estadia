from django.urls import path
from . import views

app_name = 'voluntarios'

urlpatterns = [
    path('', views.voluntario_list, name='voluntario_list'),
    path('nuevo/', views.voluntario_create, name='voluntario_create'),
    path('editar/<int:pk>/', views.voluntario_update, name='voluntario_update'),
    path('eliminar/<int:pk>/', views.voluntario_delete, name='voluntario_delete'),

    path('asignaciones/', views.asignacion_list, name='asignacion_list'),
    path('asignaciones/eliminar/<int:pk>/', views.asignacion_delete, name='asignacion_delete'),
]
