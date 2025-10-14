from django.urls import path
from . import views

urlpatterns = [
    path('general/', views.chat_general, name='chat_general'),
    path('privado/', views.chat_privado_selector, name='chat_privado_selector'),
    path('privado/<int:receptor_id>/', views.chat_privado, name='chat_privado'),
]
