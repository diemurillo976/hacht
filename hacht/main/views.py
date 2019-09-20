from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .models import Profile
from .models import Paciente_N
from .forms import RegistrationForm, Data_PacienteN
from django.http import HttpResponse

#Pyrebase and model imports#################################################
import pyrebase
from PIL import Image
from io import BytesIO
import requests
import sys
sys.path.insert(0,'/home/Martinvc96/hacht/hacht/main/CNN_src/')
import forward
from forward import *
#Firebase auth#

config = {
    "apiKey": "AIzaSyArQxRet5XqKI6v8948A2ZnHZOZsu7vCNY",
    "authDomain": "hacht-7d98d.firebaseapp.com",
    "databaseURL": "https://hacht-7d98d.firebaseio.com",
    "projectId": "hacht-7d98d",
    "storageBucket": "hacht-7d98d.appspot.com",
    "messagingSenderId": "225406534324",
    "appId": "1:225406534324:web:f5317f74d07ced54"
  }

#Firebase Storage reference#

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

##################################################################


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

            new_user.profile.rol = request.POST["rol"]
            new_user.profile.org = request.POST["org"]

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

    if request.user.is_authenticated:

        if request.method == "GET":

            all_patients_n = Paciente_N.objects.filter(id_user=request.user)
            context = {'pacientes': all_patients_n}
            return render(request, 'index/dashboard_pacientes.html', context)
        
        elif request.method == "POST":

            if request.POST.get("id"):

                id_p = request.POST["id"]
                instancia_paciente = get_object_or_404(Paciente_N, pk=id_p)
                form = Data_PacienteN(request.POST, instance=instancia_paciente)
            
            else:
                form = Data_PacienteN(request.POST)

            if(form.is_valid()):
                
                """
                new_patient = Paciente_N(id_user=request.user, 
                                        nombre=request.POST["nombre"],
                                        ced=request.POST["cedula"],
                                        sexo=request.POST["sexo"],
                                        edad=request.POST["edad"],
                                        res=request.POST["res"],)
                """

                paciente = form.save()

                paciente.id_user = request.user

                paciente.save()

                return redirect('/dashboard_pacientes/')

            else:
                print(str(form._errors))

    else:
        return HttpResponse(status=403)

def dashboard_sesiones(request):

    return render(request, 'index/dashboard_sesiones.html')

def contact_us(request):
    return render(request, 'index/contact-us.html')

def features(request):
    return render(request, 'index/features.html' )

def demo(request):
    if(request.method == "POST"):
        upload = request.FILES['upload']
        storage.child(str(upload)).put(upload)
        url = storage.child(str(upload)).get_url(None)
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        result = forward_single_img(img)
        context = {"result": result}
        return render(request, 'index/demo.html', context)
    elif(request.method == "GET"):
        return render(request, 'index/demo.html')

def descriptivo_paciente(request):
    
    # Si no hay paciente seleccionado se envía el form vacio
    if request.GET.get("id_paciente"):
        
        id_p = int(request.GET["id_paciente"])

        # Obtiene el paciente
        paciente = Paciente_N.objects.get(pk=id_p)

        # Crea el formulario
        form = Data_PacienteN(instance=paciente)

    else:
            
        # Crea el formulario
        form = Data_PacienteN()

    context = {'form': form}
    return render(request, 'index/components/descriptivo_paciente.html', context)

def eliminar_paciente(request):

    if request.POST.get("id_paciente"):

        id_p = request.POST["id_paciente"]
        paciente = Paciente_N.objects.get(pk=id_p)
        paciente.delete()
        return HttpResponse(status=204) # Se procesó correctamente pero no hay contenido

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request