from django.urls import path
from . import views

app_name = "mantenimiento"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("<str:tipo>/", views.tareas_list_tipo, name="tareas_list_tipo"),
    path("<str:tipo>/nueva/", views.tarea_create_tipo, name="tarea_create_tipo"),
    path("editar/<int:pk>/", views.tarea_update, name="tarea_update_form"),
    path("eliminar/<int:pk>/", views.tarea_delete, name="tarea_delete"),
]
