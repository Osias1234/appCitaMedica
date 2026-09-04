# clinica/models.py
from django.db import models
from usuarios.models import Usuario

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Especialidad")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Medico(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='medico_perfil',
        verbose_name="Usuario"
    )
    especialidad = models.ForeignKey(
        Especialidad, 
        on_delete=models.PROTECT, 
        related_name='medicos',
        verbose_name="Especialidad"
    )
    licencia_medica = models.CharField(max_length=50, unique=True, verbose_name="Licencia / Matrícula Médica")
    consultorio = models.CharField(max_length=50, blank=True, null=True, verbose_name="Consultorio")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # NUEVOS CAMPOS
    duracion_cita = models.PositiveIntegerField(default=30, verbose_name="Duración por cita (minutos)")
    max_horas_mes = models.PositiveIntegerField(default=120, verbose_name="Máximo horas al mes")
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    def __str__(self):
        return f"Dr(a). {self.usuario.get_full_name() or self.usuario.username} - {self.especialidad.nombre}"