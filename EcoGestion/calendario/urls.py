from django.urls import path
from . import views

app_name = "calendario"

urlpatterns = [
    path("", views.calendario_view, name="calendario"),
    path("api/tareas/", views.tareas_feed, name="tareas_feed"),
    path("api/tareas/<int:tarea_id>/done/", views.tarea_marcar_realizada, name="tarea_done"),
    path("api/tareas/<int:tarea_id>/update/", views.tarea_actualizar, name="tarea_update"),
]

