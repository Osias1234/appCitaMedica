from django import forms
from .models import Especialidad, Medico
from usuarios.models import Usuario

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Cardiología'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional de la especialidad...'
            }),
        }


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['usuario', 'especialidad', 'licencia_medica', 'consultorio', 'activo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'licencia_medica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nº de Matrícula/Licencia'
            }),
            'consultorio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Consultorio 102'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo usuarios registrados con tipo_usuario = 'MEDICO'
        self.fields['usuario'].queryset = Usuario.objects.filter(tipo_usuario='MEDICO')
        self.fields['usuario'].empty_label = "-- Seleccionar Usuario Médico --"
        self.fields['especialidad'].empty_label = "-- Seleccionar Especialidad --"