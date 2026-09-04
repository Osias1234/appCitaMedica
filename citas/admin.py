# citas/admin.py
from django.contrib import admin
from .models import Turno, CitaMedica

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('medico', 'fecha', 'hora_inicio', 'hora_fin', 'horas_totales', 'activo')
    list_filter = ('fecha', 'activo', 'medico')
    search_fields = (
        'medico__usuario__first_name', 
        'medico__usuario__last_name', 
        'medico__usuario__username'
    )

@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha', 'hora', 'estado', 'creado_el')
    list_filter = ('estado', 'fecha', 'medico')
    search_fields = (
        'paciente__usuario__first_name', 
        'paciente__usuario__last_name', 
        'medico__usuario__first_name', 
        'medico__usuario__last_name'
    )