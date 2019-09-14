from django.shortcuts import render, redirect
from .models import User
from .models import Profile
from .forms import RegistrationForm, Data_PacienteN
#hola


def index(request):
    return render(request, 'index/index.html')

def login(request):
    return render(request, 'index/login.html')

def registration(request):
    if(request.method == 'POST'):
        form = RegistrationForm(request.POST)

        if(form.is_valid()):

            # Creates the django's user
            new_user = User(username=request.POST['correo'],
                            email=request.POST['correo'],
                            first_name=request.POST['nombre'])

            new_user.set_password(request.POST['password'])
            new_user.save()

            new_user.profile.rol = 1
            new_user.profile.org = "prueba"

            new_user.save()
            print('NUEVO REGISTRO USER AGREGADO')
            #messages.success(request, _('El usuario ha sido creado con éxito'))

            return redirect('registration_success')

    if(request.method == 'GET'):
        form = RegistrationForm()

    context = {'form' : form}
    return render(request, 'index/registration.html', context)


def registration_success(request):
    return render(request, 'index/registration_success.html')

def dashboard_pacientes(request):
    form = Data_PacienteN()
    context = {'form': form}
    return render(request, 'index/dashboard_pacientes.html', context)

def dashboard_sesiones(request):
    return render(request, 'index/dashboard_sesiones.html')

def contact_us(request):
    return render(request, 'index/contact-us.html')

def features(request):
    return render(request, 'index/features.html' )