# usuarios/urls.py
from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegistroPacienteView

app_name = 'usuarios'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', RegistroPacienteView.as_view(), name='registro'),
]