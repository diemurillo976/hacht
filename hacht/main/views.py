import sys
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, Paciente, Sesion
from .forms import RegistrationForm, Data_PacienteN, Data_Comp_Sesion_Completo, Muestra, Data_Sesion_Muestra
from django.http import HttpResponse
from django.db.models import Model, Count
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.contrib.auth import authenticate, login
from django.dispatch import receiver
from django.db.models.query import QuerySet
from django.template.defaulttags import register
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
import numpy as np
import os
import csv
import time
from datetime import datetime

from .Clients import ClientFactory

#Pyrebase and model imports#################################################
import pyrebase
from PIL import Image
from io import BytesIO
import requests

#Comentado por motivos de falta de espacio en el hosting

from .CNN_src.forward import *

#Firebase auth##############################################################

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

############################################################################

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    print(credentials)
    print("Login fallado para las credenciales: {}".format(credentials))

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    print(user)
    print("Se loggeó correctamente el usuario {}".format(user))

# Auxiliar function to return a list of static images and their corresponding class
def read_static_list():

    # Obtiene el path del archivo csv con la lista
    path = os.getcwd()
    abs_path = os.path.join(path, "hacht","hacht", "main", "static", "index", "assets", "csv", "demo_src.csv")

    with open(abs_path) as file:

        reader = csv.reader(file, delimiter=',')
        lista = []

        for row in reader:

            y_true, url = row[0], row[1]
            lista.append((y_true, url))

    return lista

def ayuda(request):

    if request.user.is_authenticated:

        context = {"logged_in" : True}
        return render(request, 'index/help.html', context)

    return render(request, 'index/help.html')

# Funcion to handle error responses
def handle_error(request, status, message):

    client = ClientFactory.get_client(request)

    return client.handle_error(request, status, message)

# Function to catch the 500 internal error
def handle_500_error(request):

    return handle_error(request, status=500, message="El servidor ha tenido un problema resolviendo la petición")



def index(request):
    client = ClientFactory.get_client(request)

    return client.index(request)


def login_app(request):
    client = ClientFactory.get_client(request)

    return client.login_app(request)


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

        else:

            return handle_error(
                request,
                status=400,
                message="No se podido completar la adición del usuario, por favor revise los datos ingresados y que estos sean válidos"
            )

    if(request.method == 'GET'):
        form = RegistrationForm()

    context = {'form' : form}
    return render(request, 'index/registration.html', context)


def registration_success(request):
    return render(request, 'index/registration_success.html')

def demo(request):
    print(request)
    if request.method == "GET" and request.GET.get("resultado"):

        lista = read_static_list()

        index = int(request.GET["index"])
        y_true, url = lista[index]
        resultado = int(request.GET["resultado"])
        estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

        context = {"class": y_true,
                   "url": url,
                   "resultado": estimations[resultado],
                   "index": index}

        return render(request, 'index/components/comp_demo.html', context)

    elif request.method == "GET" and request.GET.get("index"):

        lista = read_static_list()

        index = int(request.GET["index"])
        y_true, url = lista[index]
        context = {"class": y_true,
                   "url": url,
                   "index": index}

        return render(request, 'index/components/comp_demo.html', context)

    elif request.method == "GET":

        return render(request, 'index/demo.html')

    elif request.method == "POST":

        time.sleep(1)

        index = int(request.POST["index"])
        url = request.POST["url"]

        url_fire = storage.child(url)
        response = requests.get(url)

        img = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        result = forward_single_img(img_cv)

        context = {
            "index" : index,
            "resultado" : result
        }

        return render(request, "index/demo.html", context)


def dashboard_pacientes(request):

    # Only the medic user should be seeing "patients"
    if request.user.is_authenticated and request.user.profile.rol == '0':

        if request.method == "GET":

            all_patients_n = Paciente.objects.filter(id_user=request.user)
            context = {'pacientes': all_patients_n}

            if request.GET.get("android"):
                return get_for_android(request, context)
            else:
                return render(request, 'index/dashboard_pacientes.html', context)

        elif request.method == "POST":

            if request.POST.get("id"):

                id_p = request.POST["id"]
                instancia_paciente = get_object_or_404(Paciente, pk=id_p)
                form = Data_PacienteN(request.POST, instance=instancia_paciente)

            else:

                form = Data_PacienteN(request.POST)

            if(form.is_valid()):

                paciente = form.save()
                paciente.id_user = request.user
                paciente.save()

                return redirect('/dashboard_pacientes/')

            else:

                return handle_error(
                    request,
                    status=400,
                    message="No se ha podido agregar el paciente. Se encontraron los errores: \n{}".format(str(form._errors))
                )

    # If the user is authenticated and is a medic, gets redirected to dashboard_sesiones
    elif request.user.is_authenticated:

        if request.GET.get("android"):
            return redirect('/dashboard_sesiones/?android=1', permanent=True)
        else:
            return redirect('dashboard_sesiones', permanent=True)

    else:

        return handle_error(
            request,
            status=401,
            message="El usuario no está autenticado, para acceder a esta funcionalidad primero debe ingresar con sus credenciales"
        )

def descriptivo_paciente(request):

    # Si no hay paciente seleccionado se envía el form vacio
    if request.GET.get("id_paciente"):

        id_p = int(request.GET["id_paciente"])

        # Obtiene el paciente
        paciente = Paciente.objects.get(pk=id_p)

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
        paciente = Paciente.objects.get(pk=id_p)
        paciente.delete()
        return HttpResponse(status=204) # Se procesó correctamente pero no hay contenido

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def dashboard_sesiones(request):

    if request.user.is_authenticated:

        # Si hay un id_paciente en el get entonces el método debería haber sido llamado
        # por un usuario médico. Dentro se chequea que el paciente perteneza al usuario
        if request.method == "GET" and request.GET.get("id_paciente") and request.user.profile.rol == '0':

            paciente = Paciente.objects.get(pk=request.GET["id_paciente"])

            # Evita que con la dirección correcta se obtenga el valor
            if paciente.id_user != request.user:
                return HttpResponse(status=403)

            sesiones = Sesion.objects.filter(id_paciente=request.GET["id_paciente"])
            context = {"paciente" : paciente, "sesiones" : sesiones}

            if request.GET.get("android"):

                return get_for_android(request, context)

            else:

                return render(request, 'index/dashboard_sesiones.html', context)

        # Cuando es usuario investigador
        elif request.method == "GET":

            sesiones = Sesion.objects.filter(id_usuario=request.user.id)
            context = {'sesiones' : sesiones}

            if request.GET.get("android"):

                return get_for_android(request, context)

            else:

                return render(request, 'index/dashboard_sesiones.html', context)

        elif request.method == "POST":

            if request.POST.get("id"):

                # Obtiene los datos ingresados contra los dato
                id_s = request.POST["id"]
                instancia_sesion = get_object_or_404(Sesion, pk=id_s)
                form = Data_Comp_Sesion_Completo(request.POST, instance=instancia_sesion)

            else:

                # Popula el formulario solo con los datos obtenidos del post
                form = Data_Comp_Sesion_Completo(request.POST)

            if(form.is_valid()):

                sesion = form.save()

                if request.user.profile.rol == '0':
                    id_paciente = request.POST["id_paciente"]
                    sesion.id_paciente = id_paciente
                    sesion = form.save()
                    return redirect('/dashboard_sesiones/?id_paciente=' + id_paciente)
                else:
                    id_usuario = request.user.id
                    sesion.id_usuario = id_usuario
                    sesion = form.save()
                    return redirect('/dashboard_sesiones/')

            else:
                print(str(form._errors))


            return render(request, 'index/dashboard_sesiones.html')

        else:
            return HttpResponse(status=404)

    else:
        return HttpResponse(status=403)


def descriptivo_sesion(request):

    if request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)
        form = Data_Comp_Sesion_Completo(instance=sesion)

    else:

        form = Data_Comp_Sesion_Completo()

    if request.GET.get("id_paciente"):

        id_paciente = request.GET["id_paciente"]
        context = {'form': form, 'id_paciente': id_paciente}

    else:
        context = {'form': form}

    return render(request, 'index/components/descriptivo_sesion.html', context)

def eliminar_sesion(request):

    if request.POST.get("id_sesion"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)
        sesion.delete()
        return HttpResponse(status=204) # Se procesó correctamente pero no hay contenido

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def muestras_sesion(request):

    if request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        if request.GET.get("android"):

            muestras = Muestra.objects.filter(sesion=id_s)
            context = {
                'sesion' : sesion,
                'muestras' : muestras
            }

            return get_for_android(request, context)

        else:

            muestras = []

            for muestra in Muestra.objects.filter(sesion=id_s):
                form = Data_Sesion_Muestra(instance=muestra)
                muestras.append(form)


            context = {
                'sesion' : sesion,
                'forms' : muestras
            }

            return render(request, 'index/components/muestras_sesion.html', context)

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def agregar_muestra(request):

    if request.POST.get("id_sesion"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        # Obtiene los múltiples archivos
        files = request.FILES.getlist('img_file')

        # Por cada archivo lo sube a Firebase, hace la predicción y lo agrega a la BD local
        for file in files:

            steps = 0
            exito = False
            guardada = False

            while steps < 5 and not exito:

                try:

                    if guardada == False:
                        storage.child(str(file)).put(file)
                        guardada = True

                    url = storage.child(str(file)).get_url(None)
                    response = requests.get(url)

                    img = Image.open(BytesIO(response.content))
                    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    result = forward_single_img(img_cv)
                    estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

                    muestra = Muestra(
                        sesion=sesion,
                        url_img=url,
                        pred=estimations[result],
                    )

                    muestra.save()

                    exito = True

                except:
                    steps += 1

            if not exito:
                return handle_error(request, status=500, message="Lo sentimos, no se ha podido establecer la conexión con la base de datos para imágenes. Al menos en alguna muestra se han realizado más de 5 intentos para establecer la conexión.")

        if request.user.profile.rol == '0':
            return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido
        else:
            return redirect('/dashboard_sesiones/') # Se procesó correctamente pero no hay contenido

    else:
        # Maneja el error de que no llegue id_sesion
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request

def demo_app_muestra(request):

    if request.GET.get("android") and request.GET.get("url"):

        url = request.GET["url"]
        response = requests.get(url)

        img = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        result = forward_single_img(img_cv)
        estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

        context = {
                'estimacion' : estimations[result]
            }

        return get_for_android(request, context)

    else:
        return HttpResponse(status=403)


def modificar_muestra(request):

    if request.POST.get("id_muestra") and request.POST.get("update"):

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        if request.POST.get("consent"):
            muestra.consent = request.POST["consent"]
        if request.POST.get("pred_true"):
            muestra.pred_true = request.POST["pred_true"]

        muestra.obs = request.POST["obs"]

        muestra.save()

        if request.user.profile.rol == '0':
            return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido
        else:
            return redirect('/dashboard_sesiones/')

    elif request.POST.get("id_muestra") and request.POST.get("delete"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        muestra.delete()

        return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente))

    else:

        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request


def contact_us(request):
    return render(request, 'index/contact-us.html')

def features(request):
    return render(request, 'index/features.html' )

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))
