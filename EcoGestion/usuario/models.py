from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, email, nombre_completo, password=None, rol='mantenimiento'):
        if not matricula or not email:
            raise ValueError('El usuario debe tener matrícula y correo')
        user = self.model(
            matricula=matricula,
            email=self.normalize_email(email),
            nombre_completo=nombre_completo,
            rol=rol
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, email, nombre_completo, password):
        user = self.create_user(
            matricula=matricula,
            email=email,
            nombre_completo=nombre_completo,
            password=password,
            rol='administrador'
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('administrador', 'Administrador'),
        ('gestor', 'Gestor de especies'),
        ('mantenimiento', 'Mantenimiento'),
    )
    id_usuario = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(verbose_name='email address',max_length=100, unique=True)
    nombre_completo = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=ROLES, default='mantenimiento')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UsuarioManager()

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['email', 'nombre_completo']

    def __str__(self):
        return self.nombre_completo