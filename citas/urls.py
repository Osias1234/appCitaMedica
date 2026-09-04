from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    # ADMIN
    path('admin/turnos/', views.TurnoListView.as_view(), name='turno_list'),
    path('admin/turnos/nuevo/', views.TurnoCreateView.as_view(), name='turno_create'),
    path('admin/turnos/editar/<int:pk>/', views.TurnoUpdateView.as_view(), name='turno_update'),
    path('admin/turnos/eliminar/<int:pk>/', views.TurnoDeleteView.as_view(), name='turno_delete'),

    # MÉDICO
    path('medico/agenda/', views.AgendaMedicoView.as_view(), name='agenda_medico'),
    
    path('medico/cita/<int:pk>/estado/', views.ActualizarCitaMedicoView.as_view(), name='cita_medico_update'),

    # PACIENTE
    path('mis-citas/', views.MisCitasListView.as_view(), name='mis_citas'),
    path('agendar/', views.CitaCreateView.as_view(), name='cita_create'),
    # (Opcional: Añade Update y Delete para paciente si lo deseas)
    path('cancelar/<int:pk>/', views.CitaCancelView.as_view(), name='cita_cancel'),

    # AJAX ENDPOINTS
    path('ajax/cargar-medicos/', views.cargar_medicos, name='ajax_cargar_medicos'),
    path('ajax/cargar-fechas/', views.cargar_fechas_turno, name='ajax_cargar_fechas'),
    path('ajax/cargar-horas/', views.cargar_horas_disponibles, name='ajax_cargar_horas'),
]