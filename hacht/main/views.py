import csv
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
from django.conf import settings



from .Clients import ClientFactory

#model imports#################################################

import pyrebase
from PIL import Image
from io import BytesIO
import requests


from .CNN_src.forward import *

#Firebase auth##############################################################
servicePath = os.path.join(os.getcwd(), "main", "static", "index", "assets", "json", "hacht-570b8-firebase-adminsdk-20kun-c743c4033d.json")
config = {
    "apiKey": "AIzaSyAQBVQdmZkLe3LIzcNo8LqAff86WQn9IbI",
    "authDomain": "hacht-570b8.firebaseapp.com",
    "databaseURL": "https://hacht-570b8.firebaseio.com",
    "projectId": "hacht-570b8",
    "storageBucket": "hacht-570b8.appspot.com",
    "messagingSenderId": "566493394218",
    "appId": "1:566493394218:web:535fd251874a297f205a53",
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



def ayuda(request):
    if request.user.is_authenticated:
        context = {}
        if request.user.profile.rol == '0':
            context.update({"logged_in" : "usr_doctor"})
        else:
            context.update({"logged_in" : "usr_investigador"})

        return render(request, 'index/help.html', context) # Acomodar por el cambio de logica con android y web.


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


"""
    if request.user.is_authenticated:
        context = {}
        if request.user.profile.rol == '0':
            context.update({"logged_in" : "usr_doctor"})
        else:
            context.update({"logged_in" : "usr_investigador"})
        return render(request, 'index/index.html', context) # Acomodar por el cambio de logica con android y web.

    if request.GET.get("android"):
        return get_for_android(request)
    else:
        return render(request, 'index/index.html')
"""

def login_app(request):
    client = ClientFactory.get_client(request)

    return client.login_app(request)


def registration(request):
    client = ClientFactory.get_client(request)

    return client.registration(request)


def registration_success(request):
    client = ClientFactory.get_client(request)

    return client.registration_success(request)

def demo(request):
    """
    # Codigo se encarga de leer carpeta de imagenes, las sube a firebase y guardar las referencias en un csv temporal.
    path = settings.STATIC_ROOT
    abs_path = os.path.join(path, "index", "assets", "img", "Demo_imgs", "100x")

    for file in os.listdir(abs_path):
        storage.child("Demo_subset/"+str(file)).put(os.path.join(abs_path, file))

        csv_line = {
            'metadata': 'palabra',
            'link': storage.child("Demo_subset/"+str(file)).get_url(None)
        }

        csv_path = os.path.join(path, "index", "assets", "csv", "demo_temp.csv")
        with open(csv_path, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['metadata', 'link'])
            writer.writerow(csv_line)
    # ------------------------------------------------------------------------------
    """

    client = ClientFactory.get_client(request)
    return client.demo(request)

def dashboard_pacientes(request):
    # Only the medic user should be seeing "patients"
    #client = ClientFactory.get_client(request)

    #return client.demo(request) 

    # Only the medic user should be seeing "patients"
    context = {}
    if request.user.is_authenticated and request.user.profile.rol == '0':
        context.update({"logged_in" : "usr_doctor"})

        if request.method == "GET":

            all_patients_n = Paciente.objects.filter(id_user=request.user)
            context.update({'pacientes': all_patients_n})

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

                return redirect('/dashboard_pacientes/', context)

            else:

                return handle_error(
                    request,
                    status=400,
                    message="No se ha podido agregar el paciente. Se encontraron los errores: \n{}".format(str(form._errors))
                )
    
    # If the user is authenticated and is an investigator, gets redirected to dashboard_sesiones.
    elif request.user.is_authenticated:
        context.update({"logged_in" : "usr_investigador"})

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
            context = {"paciente" : paciente, "sesiones" : sesiones, "logged_in" : "usr_doctor"}

            if request.GET.get("android"):

                return get_for_android(request, context)

            else:

                return render(request, 'index/dashboard_sesiones.html', context)

        # Cuando es usuario investigador
        elif request.method == "GET":

            sesiones = Sesion.objects.filter(id_usuario=request.user.id)
            context = {'sesiones' : sesiones, "logged_in" : "usr_investigador"}
            
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
                        settings.FIREBASE_STORAGE.child(str(file)).put(file)
                        guardada = True

                    url = settings.FIREBASE_STORAGE.child(str(file)).get_url(None)
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
    if request.user.is_authenticated:
        context = {}
        if request.user.profile.rol == '0':
            context.update({"logged_in" : "usr_doctor"})
        else:
            context.update({"logged_in" : "usr_investigador"})

        return render(request, 'index/contact-us.html', context) # Acomodar por el cambio de logica con android y web.


    return render(request, 'index/contact-us.html')

def features(request):
    if request.user.is_authenticated:
        context = {}
        if request.user.profile.rol == '0':
            context.update({"logged_in" : "usr_doctor"})
        else:
            context.update({"logged_in" : "usr_investigador"})

        return render(request, 'index/features.html', context) # Acomodar por el cambio de logica con android y web.

    return render(request, 'index/features.html' )

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))
