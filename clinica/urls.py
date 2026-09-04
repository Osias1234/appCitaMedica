from django.urls import path
from .views import (
    InicioView,
    # Especialidades
    ListaEspecialidadesView,
    CrearEspecialidadView,
    EditarEspecialidadView,
    EliminarEspecialidadView,
    # Médicos
    ListaMedicosView,
    CrearMedicoView,
    EditarMedicoView,
    EliminarMedicoView,
)

app_name = 'clinica'

urlpatterns = [
    # Inicio
    path('', InicioView.as_view(), name='inicio'),

    # Especialidades (CRUD)
    path('especialidades/', ListaEspecialidadesView.as_view(), name='lista_especialidades'),
    path('especialidades/crear/', CrearEspecialidadView.as_view(), name='crear_especialidad'),
    path('especialidades/<int:pk>/editar/', EditarEspecialidadView.as_view(), name='editar_especialidad'),
    path('especialidades/<int:pk>/eliminar/', EliminarEspecialidadView.as_view(), name='eliminar_especialidad'),

    # Médicos (CRUD)
    path('medicos/', ListaMedicosView.as_view(), name='lista_medicos'),
    path('medicos/crear/', CrearMedicoView.as_view(), name='crear_medico'),
    path('medicos/<int:pk>/editar/', EditarMedicoView.as_view(), name='editar_medico'),
    path('medicos/<int:pk>/eliminar/', EliminarMedicoView.as_view(), name='eliminar_medico'),
]