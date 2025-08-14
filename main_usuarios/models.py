from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models





class UsuarioSistemaManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UsuarioSistema(AbstractUser):
    """
    Modelo simple de usuario para el sistema de login.
    Incluye campos básicos como usuario, email y contraseña.
    """
    username = models.CharField(max_length=30, unique=True, verbose_name="Usuario", default="usuario_temp")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioSistemaManager()

    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email}"
