from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm


def index(request):
    return render(request, 'index/index.html')

def login(request):
    return render(request, 'index/login.html')


def registration(request):
    if(request.method == 'POST'):
        form = RegistrationForm(request.POST)

        if(form.is_valid()):
            new_user = User(nombre=request.POST['nombre'],
                            correo=request.POST['correo'],
                            password=request.POST['password'],
                            org=request.POST['org'],
                            rol=request.POST['rol'],
                            salt='default')
            new_user.salt = 'prueba'
            new_user.save()
            print('NUEVO REGISTRO USER AGREGADO')
            return redirect('index')

    if(request.method == 'GET'):
        form = RegistrationForm()

    context = {'form' : form}
    return render(request, 'index/registration.html', context)

def dashboard_pacientes(request):
    return render(request, 'index/dashboard_pacientes.html')

def dashboard_sesiones(request):
    return render(request, 'index/dashboard_sesiones.html')