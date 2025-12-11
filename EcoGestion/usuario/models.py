from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# UsuarioManager: manejador personalizado para crear usuarios y superusuarios.
class UsuarioManager(BaseUserManager):
    # create_user(matricula, email, nombre_completo, password=None, rol='mantenimiento'):
    # Crea un usuario regular con matricula, correo, nombre y rol.
    # Entrada: datos de registro y contrasena opcional. Salida: instancia de Usuario guardada.
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

    # create_superuser(matricula, email, nombre_completo, password):
    # Crea un superusuario con permisos administrativos completos.
    # Entrada: datos requeridos y contrasena. Salida: instancia de Usuario con is_staff/is_superuser.
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

# Usuario: modelo de usuario personalizado con roles para la aplicacion.
# Campos principales: matricula como USERNAME_FIELD, email, nombre completo, rol y flags de estado.
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

    # __str__(): devuelve el nombre completo para representar al usuario.
    def __str__(self):
        return self.nombre_completo
