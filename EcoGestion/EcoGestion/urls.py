from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('login', permanent=False)),  
    path('account/', include('usuario.urls')),
    path('admin/', admin.site.urls),
    path('plants/', include('plantas.urls')),
    path('chat/', include('chat.urls')),
    path('calendario/', include('calendario.urls')),
    path('mantenimiento/', include('mantenimiento.urls')),
    path('incidencias/', include('incidencias.urls')),
    path('herramientas/', include('herramientas.urls')),
    path('salud/', include('salud.urls')), 
    path('productos/', include('productos.urls')),
    path('voluntarios/', include('voluntarios.urls')),
    path('backup/', include('respaldo.urls')),
    path('reportes/', include('reportes.urls')),
    path("notificaciones/", include("notificaciones.urls", namespace="notificaciones")),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:  # solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Servir estáticos desde STATIC_ROOT sin WhiteNoise (entorno local/Daphne)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
