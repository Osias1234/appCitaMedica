from django.shortcuts import render

# Create your views here.
# usuarios/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegistroPacienteForm, CustomLoginForm

class CustomLoginView(LoginView):
    """
    Vista CBV para el inicio de sesión del sistema.
    """
    form_class = CustomLoginForm
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """
    Cierra la sesión activa y redirige al inicio.
    """
    next_page = reverse_lazy('clinica:inicio')


class RegistroPacienteView(SuccessMessageMixin, CreateView):
    """
    Vista CBV para el registro público de nuevos pacientes.
    """
    form_class = RegistroPacienteForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:login')
    success_message = "¡Tu cuenta ha sido registrada con éxito! Ahora puedes iniciar sesión."