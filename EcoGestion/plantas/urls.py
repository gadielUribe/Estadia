from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('create/', views.crear, name='crear'),
    path('<int:id_arbol>/edit/', views.editar, name='editar'),
    path('<int:id_arbol>/delete/', views.eliminar, name='eliminar')
]