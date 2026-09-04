from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Paciente

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class RegistroPacienteForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nombre(s)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, label="Apellido(s)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ci = forms.CharField(max_length=20, required=True, label="Cédula de Identidad", widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono", widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Campos adicionales que guardaremos en la tabla Paciente
    fecha_nacimiento = forms.DateField(
        required=False, 
        label="Fecha de Nacimiento", 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    direccion = forms.CharField(
        max_length=255, 
        required=False, 
        label="Dirección", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contacto_emergencia = forms.CharField(
        max_length=100, 
        required=False, 
        label="Contacto de Emergencia", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        # Únicamente campos que existen en el modelo Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'ci', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.tipo_usuario = 'PACIENTE'
        if commit:
            usuario.save()
            Paciente.objects.create(
                usuario=usuario,
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
                direccion=self.cleaned_data.get('direccion'),
                contacto_emergencia=self.cleaned_data.get('contacto_emergencia')
            )
        return usuario