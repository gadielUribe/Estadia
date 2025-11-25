from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('nuevo/', views.producto_create, name='producto_create'),
    path('editar/<int:pk>/', views.producto_update, name='producto_update'),
    path('eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('existencias/<int:pk>/', views.producto_stock_update, name='producto_stock_update'),
    # Se eliminan rutas de asignaciones para simplificar flujo
    # Ver tareas que usan un producto específico
    path('<int:pk>/tareas/', views.producto_tareas, name='producto_tareas'),
]
