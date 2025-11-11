from django.urls import path
from . import views

app_name = "mantenimiento"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("tareas/", views.tareas_list, name="tareas_list"),
    path("tareas/nueva/", views.tarea_create, name="tarea_create"),
    path("tareas/editar/<int:pk>/", views.tarea_update, name="tarea_update_form"),
    path("tareas/eliminar/<int:pk>/", views.tarea_delete, name="tarea_delete"),
]
