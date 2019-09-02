from django import forms

roles= [
    ('0', 'Médico'),
    ('1', 'Investigador')
    ]

class RegistrationForm(forms.Form):
    nombre = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item' }))
    correo = forms.EmailField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item', 'type' : 'email' }))
    password = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class' : 'form-control item',  'type' : 'password' }))
    org = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control item' }))
    rol = forms.CharField(widget=forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle', 'data-toggle' : 'dropdown', 'aria-expanded' : 'false', 'type' : 'button', 'style' : 'height: 37px;'}, choices=roles))