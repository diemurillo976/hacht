from django import forms
from .models import *

roles= [
    ('0', 'Médico'),
    ('1', 'Investigador')
    ]

sexo=[
    ('0', 'M'),
    ('1', 'F'),
    ('2', 'N/A')
]

estados=[
    ('0','Seguro'),
    ('1','Moderado'),
    ('2','Riesgoso')
]

class RegistrationForm(forms.Form):

    """
    class Meta:

        model= Paciente_N
        fields = ("nombre", "correo", "password", "org", "rol")
        widgets= {
            "nombre" : forms.TextInput(attrs={'class' : 'form-control item' }),
            "correo" :
            "password" :
            "org" :
            "rol" :
        }
    """

    nombre = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item' }))
    correo = forms.EmailField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item', 'type' : 'email', 'id' : 'email'}))
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control item',  'type' : 'password' }))
    org = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control item' }))
    rol = forms.CharField(widget=forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=roles))

class Data_PacienteN(forms.ModelForm):

    class Meta:

        model= Paciente_N
        fields = ["id", "ced", "nombre", "res", "edad", "sexo"]
        widgets = {
            "id" : forms.HiddenInput(),
            "ced" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "nombre" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "res" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "edad" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "sexo" : forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=sexo)
        }
        
class Data_Comp_Sesion(forms.Form):

    fecha = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    estado = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))

class Data_Comp_Sesion_Completo(forms.Form):

    fecha = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    estado = forms.CharField(widget=forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=estados))
    observacion = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class':'form-control', 'type':'text'}))

class Data_Sesion_Muestra(forms.Form):

    prediccion = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    observacion = forms.CharField(max_length=400, widget=forms.Textarea(attrs={'class':'form-control', 'type':'text'}))