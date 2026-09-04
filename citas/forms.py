from django import forms
from .models import Turno, CitaMedica
from clinica.models import Especialidad, Medico

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['medico', 'fecha', 'hora_inicio', 'hora_fin', 'activo']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class CitaMedicoEstadoForm(forms.ModelForm):
    """Formulario para que el médico actualice el estado de la cita"""
    class Meta:
        model = CitaMedica
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'})
        }

class CitaPacienteForm(forms.ModelForm):
    """Formulario dinámico para que el paciente agende"""
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        empty_label="Seleccione Especialidad",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_especialidad'})
    )
    
    class Meta:
        model = CitaMedica
        fields = ['especialidad', 'medico', 'fecha', 'hora', 'motivo']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-select', 'id': 'id_medico'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_fecha'}),
            # La hora la enviaremos oculta desde los botones generados por JS, o como input read-only
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'id_hora', 'readonly': True}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descripción de su dolencia o motivo...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicialmente vaciamos los choices para que se llenen vía AJAX
        self.fields['medico'].queryset = Medico.objects.none()
        
        if 'especialidad' in self.data:
            try:
                especialidad_id = int(self.data.get('especialidad'))
                self.fields['medico'].queryset = Medico.objects.filter(especialidad_id=especialidad_id, activo=True)
            except (ValueError, TypeError):
                pass