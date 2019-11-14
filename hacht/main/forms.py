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
    ('0', 'Seguro'),
    ('1', 'Moderado'),
    ('2', 'Riesgoso')
]

booleano = [
    (1, 'Si'),
    (0, 'No')
]

estimations = [
    (None, "No seleccionado"),
    ("Adenosis", "Adenosis"),
    ("Fibroadenoma", "Fibroadenoma"),
    ("Phyllodes Tumour", "Phyllodes Tumour"),
    ("Tubular Adenon", "Tubular Adenon"),
    ("Carcinoma", "Carcinoma"),
    ("Lobular Carcinoma", "Lobular Carcinoma"),
    ("Mucinous Carcinoma", "Mucinous Carcinoma"),
    ("Papillary Carcinoma", "Papillary Carcinoma")
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

    nombre = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item', 'pattern' : '[A-Za-z ]+', 'title' : 'Ingrese caracteres solamente' }))
    correo = forms.EmailField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item', 'type' : 'email', 'id' : 'email'}))
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control item',  'type' : 'password' }))
    org = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control item' }))
    rol = forms.CharField(widget=forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=roles))

class Data_PacienteN(forms.ModelForm):

    class Meta:

        model= Paciente
        fields = ["id", "ced", "nombre", "res", "edad", "sexo"]
        widgets = {
            "id" : forms.HiddenInput(),
            "ced" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "nombre" : forms.TextInput(attrs={'class':'form-control', 'type':'text', 'pattern' : '[A-Za-z ]*'}), 
            "res" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "edad" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}), 
            "sexo" : forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=sexo)
        }


class Data_Comp_Sesion_Completo(forms.ModelForm):

    class Meta:

        model = Sesion
        fields = ["id", "date", "obs", "estado"]
        widgets = {
            "date" : forms.DateInput(format='%Y-%m-%d', attrs={'class':'form-control', 'type':'date'}),
            "estado" : forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=estados),
            "obs" : forms.Textarea(attrs={'class':'form-control', 'type':'text', 'style':'max-height: 75px'})
        }

class Data_Sesion_Muestra(forms.ModelForm):

    class Meta:

        model = Muestra
        fields = ["id", "url_img", "pred", "obs", "pred_true", "consent"]
        widgets = {
            "pred" : forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            "obs" : forms.Textarea(attrs={'class':'form-control', 'type':'text', 'style':'height: 75px'}),
            "pred_true" : forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=estimations),
            "consent" : forms.RadioSelect(attrs={'class' : 'form-check form-check-inline radio-propio'}, choices=booleano)  
        }
        