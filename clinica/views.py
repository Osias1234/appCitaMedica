from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Especialidad, Medico
from .froms import EspecialidadForm, MedicoForm


# --- MIXIN DE SEGURIDAD PARA ADMINISTRADORES ---
class EsAdminMixin(UserPassesTestMixin):
    """
    Mixin para restringir el acceso a vistas de gestión solo a Administradores.
    """
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser or 
            user.is_staff or 
            getattr(user, 'tipo_usuario', None) == 'ADMIN'
        )

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos de administrador para realizar esta acción.")
        return super().handle_no_permission()


# --- VISTA DE INICIO (LANDING PAGE) ---
class InicioView(TemplateView):
    template_name = 'clinica/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especialidades_destacadas'] = Especialidad.objects.all()[:6]
        context['medicos_destacados'] = Medico.objects.filter(activo=True).select_related('usuario', 'especialidad')[:4]
        return context


# ==========================================
# CRUD ESPECIALIDADES
# ==========================================

class ListaEspecialidadesView(ListView):
    """Pública: Listado de especialidades médicas."""
    model = Especialidad
    template_name = 'clinica/lista_especialidades.html'
    context_object_name = 'especialidades'


class CrearEspecialidadView(EsAdminMixin, SuccessMessageMixin, CreateView):
    """Solo Admin: Crear una nueva especialidad."""
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'clinica/especialidad_form.html'
    success_url = reverse_lazy('clinica:lista_especialidades')
    success_message = "Especialidad creada correctamente."


class EditarEspecialidadView(EsAdminMixin, SuccessMessageMixin, UpdateView):
    """Solo Admin: Editar una especialidad existente."""
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'clinica/especialidad_form.html'
    success_url = reverse_lazy('clinica:lista_especialidades')
    success_message = "Especialidad actualizada correctamente."


class EliminarEspecialidadView(EsAdminMixin, DeleteView):
    """Solo Admin: Eliminar una especialidad."""
    model = Especialidad
    template_name = 'clinica/especialidad_confirm_delete.html'
    success_url = reverse_lazy('clinica:lista_especialidades')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "La especialidad ha sido eliminada.")
        return super().delete(request, *args, **kwargs)


# ==========================================
# CRUD MÉDICOS
# ==========================================

class ListaMedicosView(ListView):
    """Pública: Directorio de médicos con filtros."""
    model = Medico
    template_name = 'clinica/lista_medicos.html'
    context_object_name = 'medicos'

    def get_queryset(self):
        queryset = Medico.objects.select_related('usuario', 'especialidad').all()
        especialidad_id = self.request.GET.get('especialidad')
        query = self.request.GET.get('q')

        if especialidad_id:
            queryset = queryset.filter(especialidad_id=especialidad_id)
        if query:
            queryset = queryset.filter(
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(especialidad__nombre__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especialidades'] = Especialidad.objects.all()
        return context


class CrearMedicoView(EsAdminMixin, SuccessMessageMixin, CreateView):
    """Solo Admin: Registrar un nuevo perfil médico."""
    model = Medico
    form_class = MedicoForm
    template_name = 'clinica/medico_form.html'
    success_url = reverse_lazy('clinica:lista_medicos')
    success_message = "Perfil de médico creado exitosamente."


class EditarMedicoView(EsAdminMixin, SuccessMessageMixin, UpdateView):
    """Solo Admin: Editar la información de un médico."""
    model = Medico
    form_class = MedicoForm
    template_name = 'clinica/medico_form.html'
    success_url = reverse_lazy('clinica:lista_medicos')
    success_message = "Información del médico actualizada."


class EliminarMedicoView(EsAdminMixin, DeleteView):
    """Solo Admin: Eliminar un registro médico."""
    model = Medico
    template_name = 'clinica/medico_confirm_delete.html'
    success_url = reverse_lazy('clinica:lista_medicos')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "El registro médico ha sido eliminado.")
        return super().delete(request, *args, **kwargs)