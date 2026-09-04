# citas/models.py
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from usuarios.models import Paciente
from clinica.models import Medico

class Turno(models.Model):
    medico = models.ForeignKey(
        Medico, 
        on_delete=models.CASCADE, 
        related_name='turnos', 
        verbose_name="Médico"
    )
    fecha = models.DateField(verbose_name="Fecha del Turno", default=date.today)
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Turno de Atención"
        verbose_name_plural = "Turnos de Atención"
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"Dr(a). {self.medico.usuario.get_full_name() or self.medico.usuario.username} - {self.fecha.strftime('%d/%m/%Y')} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"

    @property
    def horas_totales(self):
        """Calcula cuántas horas representa este turno."""
        dt_inicio = datetime.combine(self.fecha, self.hora_inicio)
        dt_fin = datetime.combine(self.fecha, self.hora_fin)
        diferencia = dt_fin - dt_inicio
        return round(diferencia.total_seconds() / 3600, 2)

    def clean(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

    def obtener_bloques_horarios(self):
        """
        Genera los slots de tiempo (ej. 08:00, 08:30, 09:00...) 
        según la duración de cita configurada en el médico.
        """
        bloques = []
        duracion = timedelta(minutes=self.medico.duracion_cita)
        
        actual = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)

        while actual + duracion <= fin:
            bloques.append(actual.time())
            actual += duracion
            
        return bloques


class CitaMedica(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        related_name='citas', 
        verbose_name="Paciente"
    )
    medico = models.ForeignKey(
        Medico, 
        on_delete=models.CASCADE, 
        related_name='citas', 
        verbose_name="Médico"
    )
    fecha = models.DateField(verbose_name="Fecha de la Cita")
    hora = models.TimeField(verbose_name="Hora de la Cita")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo de la Consulta")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name="Estado")
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cita Médica"
        verbose_name_plural = "Citas Médicas"
        ordering = ['-fecha', '-hora']
        unique_together = ['medico', 'fecha', 'hora']

    def __str__(self):
        return f"Cita #{self.id} - {self.paciente.usuario.get_full_name() or self.paciente.usuario.username} con Dr. {self.medico.usuario.get_full_name() or self.medico.usuario.username}"