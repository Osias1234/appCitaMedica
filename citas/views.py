from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
from django.views.generic import ListView



from .models import Turno, CitaMedica
from .forms import TurnoForm, CitaPacienteForm, CitaMedicoEstadoForm
from clinica.models import Medico

# ================= PERMISOS (MIXINS) =================
class RoleRequiredMixin(UserPassesTestMixin):
    rol_requerido = None
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.tipo_usuario == self.rol_requerido

class AdminRequiredMixin(RoleRequiredMixin):
    rol_requerido = 'ADMIN'

class MedicoRequiredMixin(RoleRequiredMixin):
    rol_requerido = 'MEDICO'

class PacienteRequiredMixin(RoleRequiredMixin):
    rol_requerido = 'PACIENTE'

# ================= PANEL ADMIN: CRUD TURNOS =================
class TurnoListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Turno
    template_name = 'citas/admin/turno_list.html'
    context_object_name = 'turnos'

class TurnoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'citas/admin/turno_form.html'
    success_url = reverse_lazy('citas:turno_list')

class TurnoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'citas/admin/turno_form.html'
    success_url = reverse_lazy('citas:turno_list')

class TurnoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Turno
    template_name = 'citas/admin/turno_confirm_delete.html'
    success_url = reverse_lazy('citas:turno_list')

# ================= PANEL MÉDICO =================
class AgendaMedicoView(LoginRequiredMixin, ListView):
    model = CitaMedica  # Cambia a CitaMedica si ese es el nombre exacto de tu modelo de citas
    template_name = 'citas/medico/agenda.html'  # Asegúrate de que coincida con la ruta de tu template
    context_object_name = 'citas'

    def get_queryset(self):
        # Obtiene el médico asociado al usuario que ha iniciado sesión
        try:
            medico = Medico.objects.get(usuario=self.request.user)
            queryset = CitaMedica.objects.filter(medico=medico)
        except Medico.DoesNotExist:
            return CitaMedica.objects.none()

        # Capturar los parámetros de filtro enviados por GET desde el template
        paciente_query = self.request.GET.get('paciente', '').strip()
        fecha_query = self.request.GET.get('fecha', '').strip()
        estado_query = self.request.GET.get('estado', '').strip()

        # Aplicar filtros si existen
        if paciente_query:
            queryset = queryset.filter(
                Q(paciente__usuario__first_name__icontains=paciente_query) |
                Q(paciente__usuario__last_name__icontains=paciente_query) |
                Q(paciente__usuario__username__icontains=paciente_query)
            )
        if fecha_query:
            queryset = queryset.filter(fecha=fecha_query)
        
        if estado_query:
            queryset = queryset.filter(estado=estado_query)

        return queryset.order_by('-fecha', '-hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añade los turnos activos del médico para mostrarlos en la columna lateral
        try:
            medico = Medico.objects.get(usuario=self.request.user)
            context['mis_turnos'] = Turno.objects.filter(medico=medico, activo=True).order_by('fecha', 'hora_inicio')
        except Medico.DoesNotExist:
            context['mis_turnos'] = []
        return context

class ActualizarCitaMedicoView(LoginRequiredMixin, MedicoRequiredMixin, UpdateView):
    model = CitaMedica
    form_class = CitaMedicoEstadoForm
    template_name = 'citas/medico/actualizar_cita.html'
    success_url = reverse_lazy('citas:agenda_medico')

# ================= PANEL PACIENTE =================
class MisCitasListView(LoginRequiredMixin, PacienteRequiredMixin, ListView):
    model = CitaMedica
    template_name = 'citas/paciente/mis_citas.html'
    context_object_name = 'citas'

    def get_queryset(self):
        paciente_perfil = getattr(self.request.user, 'paciente_perfil', None)
        # Búsqueda simple
        q = self.request.GET.get('q', '')
        qs = CitaMedica.objects.filter(paciente=paciente_perfil)
        if q:
            qs = qs.filter(medico__especialidad__nombre__icontains=q)
        return qs.order_by('-fecha', '-hora')

class CitaCreateView(LoginRequiredMixin, PacienteRequiredMixin, CreateView):
    model = CitaMedica
    form_class = CitaPacienteForm
    template_name = 'citas/paciente/cita_form.html'
    success_url = reverse_lazy('citas:mis_citas')

    def form_valid(self, form):
        # Asignar automáticamente el paciente logueado
        form.instance.paciente = self.request.user.paciente_perfil
        return super().form_valid(form)

# ================= ENDPOINTS AJAX (MAGIA DE RESERVAS) =================
def cargar_medicos(request):
    especialidad_id = request.GET.get('especialidad_id')
    medicos = Medico.objects.filter(especialidad_id=especialidad_id, activo=True).order_by('usuario__first_name')
    data = [{'id': m.id, 'nombre': f"Dr(a). {m.usuario.get_full_name()}"} for m in medicos]
    return JsonResponse(data, safe=False)

def cargar_fechas_turno(request):
    medico_id = request.GET.get('medico_id')
    turnos = Turno.objects.filter(medico_id=medico_id, activo=True, fecha__gte=datetime.today().date()).order_by('fecha')
    data = [{'fecha': t.fecha.strftime('%Y-%m-%d')} for t in turnos]
    return JsonResponse(data, safe=False)

def cargar_horas_disponibles(request):
    medico_id = request.GET.get('medico_id')
    fecha_str = request.GET.get('fecha')
    
    if not medico_id or not fecha_str:
        return JsonResponse({'horas': []})

    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    turno = Turno.objects.filter(medico_id=medico_id, fecha=fecha_obj, activo=True).first()
    
    if not turno:
        return JsonResponse({'horas': []})

    # Citas que ya están confirmadas o pendientes para esa fecha/médico
    citas_ocupadas = CitaMedica.objects.filter(
        medico_id=medico_id, fecha=fecha_obj
    ).exclude(estado='CANCELADA').values_list('hora', flat=True)

    bloques = turno.obtener_bloques_horarios()
    horas_data = []
    
    for bloque in bloques:
        # Aquí evaluamos el color: si está en citas_ocupadas es False (rojo), sino True (azul)
        horas_data.append({
            'hora': bloque.strftime('%H:%M'),
            'disponible': bloque not in citas_ocupadas
        })

    return JsonResponse({'horas': horas_data})


class TurnoListView(ListView):
    model = Turno
    template_name = 'citas/admin/turno_list.html'
    context_object_name = 'turnos'

    def get_queryset(self):
        # 1. Obtener la consulta base de turnos
        queryset = super().get_queryset()
        
        # 2. Capturar los valores enviados por el formulario GET
        medico_query = self.request.GET.get('medico', '').strip()
        fecha_query = self.request.GET.get('fecha', '').strip()

        # 3. Aplicar filtro de texto (Busca en nombre, apellido o especialidad)
        if medico_query:
            queryset = queryset.filter(
                Q(medico__usuario__first_name__icontains=medico_query) |
                Q(medico__usuario__last_name__icontains=medico_query) |
                Q(medico__especialidad__nombre__icontains=medico_query)
            )

        # 4. Aplicar filtro de fecha exacta
        if fecha_query:
            queryset = queryset.filter(fecha=fecha_query)

        # 5. Retornar los datos filtrados, ordenados por fecha
        return queryset.order_by('fecha', 'hora_inicio')
    

class CitaCancelView(LoginRequiredMixin, DeleteView):
    model = CitaMedica  # Asegúrate de que coincida con el nombre de tu modelo de citas
    template_name = 'citas/paciente/cita_cancel.html'  # Reemplaza con la ruta de tu template si es diferente
    success_url = reverse_lazy('citas:mis_citas')

    def get_queryset(self):
        # Restringe para que el paciente solo pueda eliminar/cancelar sus propias citas
        return CitaMedica.objects.filter(paciente__usuario=self.request.user)