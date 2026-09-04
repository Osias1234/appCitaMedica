from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('PACIENTE', 'Paciente'),
        ('MEDICO', 'Médico'),
        ('ADMIN', 'Administrador'),
    ]

    ci = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="Cédula de Identidad"
    )
    telefono = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        verbose_name="Teléfono / Celular"
    )
    tipo_usuario = models.CharField(
        max_length=10, 
        choices=TIPO_USUARIO_CHOICES, 
        default='PACIENTE',
        verbose_name="Tipo de Usuario"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        nombre_completo = self.get_full_name()
        return f"{nombre_completo if nombre_completo else self.username} ({self.get_tipo_usuario_display()})"


class Paciente(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='paciente_perfil',
        verbose_name="Usuario"
    )
    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Nacimiento"
    )
    direccion = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Dirección de Domicilio"
    )
    contacto_emergencia = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Contacto de Emergencia"
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"Paciente: {self.usuario.get_full_name() or self.usuario.username}"