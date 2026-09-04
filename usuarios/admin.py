from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Paciente

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Contacto e Identidad', {'fields': ('ci', 'telefono', 'tipo_usuario')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Contacto e Identidad', {'fields': ('ci', 'telefono', 'tipo_usuario')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'ci', 'tipo_usuario', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'ci', 'email')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_nacimiento', 'direccion', 'contacto_emergencia')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'usuario__ci')