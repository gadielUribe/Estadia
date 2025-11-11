from .models import Notificacion


def notificaciones_count(request):
    if not request.user.is_authenticated:
        return {"notif_unread_count": 0}
    try:
        count = Notificacion.objects.filter(destiny=request.user, eliminar=False, no_leido=True).count()
    except Exception:
        count = 0
    return {"notif_unread_count": count}

