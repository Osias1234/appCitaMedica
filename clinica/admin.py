# clinica/admin.py
from django.contrib import admin
from .models import Especialidad, Medico

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'especialidad', 'licencia_medica', 'consultorio', 'activo')
    list_filter = ('especialidad', 'activo')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'licencia_medica')