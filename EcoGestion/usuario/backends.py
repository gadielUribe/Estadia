from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class MatriculaBackend(ModelBackend):
    def authenticate(self, request, matricula=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(matricula=matricula)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None