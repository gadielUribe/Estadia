from django.urls import path
from . import views

app_name = "notificaciones"

urlpatterns = [
    path("", views.lista_notificaciones, name="lista"),
    path("marcar-leida/<int:pk>/", views.marcar_leida, name="marcar_leida"),
    path("marcar-no-leida/<int:pk>/", views.marcar_no_leida, name="marcar_no_leida"),
    path("marcar-todo-leido/", views.marcar_todo_leido, name="marcar_todo_leido"),
    path("marcar-todo-no-leido/", views.marcar_todo_no_leido, name="marcar_todo_no_leido"),
]