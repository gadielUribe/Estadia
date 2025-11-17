from django.urls import path

from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.evento_list, name="lista"),
    path("nuevo/", views.evento_create, name="crear"),
    path("<int:pk>/editar/", views.evento_update, name="editar"),
    path("<int:pk>/eliminar/", views.evento_delete, name="eliminar"),
    path("api/eventos/", views.eventos_feed, name="feed"),
]
