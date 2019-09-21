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

booleano = [
    (True, 'Si'),
    (False, 'No')
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
<<<<<<< HEAD
        
class Data_Comp_Sesion(forms.Form):
=======
>>>>>>> f3ff5ef6f8efec4ca9506d6b8a126b8ef25e5c3c

class Data_Comp_Sesion_Completo(forms.ModelForm):

    class Meta:

        model = Sesion
        fields = ["id", "date", "obs", "estado"]
        widgets = {
            "date" : forms.DateInput(format='%m/%d/%Y', attrs={'class':'form-control', 'type':'date'}),
            "estado" : forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=estados),
            "obs" : forms.Textarea(attrs={'class':'form-control', 'type':'text', 'style':'max-height: 75px'})
        }

class Data_Sesion_Muestra(forms.Form):

    class Meta:

        model = Muestra
        fields = ["id", "pred", "obs", "is_true", "consent"]
        widgets = {
            "pred" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            "obs" : forms.Textarea(attrs={'class':'form-control', 'type':'text', 'style':'max-height: 75px'}),
            "is_true" : forms.RadioSelect(attrs={'class' : 'form-check form-check-inline', 'style' : 'max-width: 95px;'}, choices=booleano),
            "consent" : forms.RadioSelect(attrs={'class' : 'form-check form-check-inline', 'style' : 'max-width: 95px;'}, choices=booleano)  
        }