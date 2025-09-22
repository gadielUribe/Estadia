from django.urls import path
from . import views

urlpatterns = [
    path('general/', views.chat_general, name='chat_general'),
    path('privado/<int:receptor_id>/', views.chat_privado, name='chat_privado'),
]