import sys
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, Paciente_N, Sesion
from .forms import RegistrationForm, Data_PacienteN, Data_Comp_Sesion_Completo, Muestra, Data_Sesion_Muestra
from django.http import HttpResponse
from django.db.models import Count, Sum
import random
import json
import numpy as np
import os
import csv
import time
from datetime import datetime

#Pyrebase and model imports#################################################
import pyrebase
from PIL import Image
from io import BytesIO
import requests

#Comentado por motivos de falta de espacio en el hosting
#sys.path.insert(0,'/home/Martinvc96/hacht/hacht/main/CNN_src/')
#sys.path.insert(0,'C:/Users/gmc_2/source/repos/HACHT/hacht/hacht/main/CNN_src/')

# Define el path a CNN_src y lo agrega al sys.path
path = os.getcwd()
path = os.path.join(path, "hacht", "hacht", "main", "CNN_src")
sys.path.insert(0, path)
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

def read_static_list():

    # Obtiene el path del archivo csv con la lista
    path = os.getcwd()
    abs_path = os.path.join(path, "hacht", "hacht", "main", "static", "index", "assets", "csv", "demo_src.csv")

    with open(abs_path) as file:

        reader = csv.reader(file, delimiter=',')
        lista = []
        
        for row in reader:

            y_true, url = row[0], row[1]
            lista.append((y_true, url))

    return lista


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

def demo(request):

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

def dashboard_sesiones(request):

    if request.user.is_authenticated:

        if request.method == "GET" and request.GET.get("id_paciente"):

            paciente = Paciente_N.objects.get(pk=request.GET["id_paciente"])
            sesiones = Sesion.objects.filter(id_paciente=request.GET["id_paciente"])
            context = {"paciente" : paciente, "sesiones" : sesiones}

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
                
                """
                new_patient = Paciente_N(id_user=request.user, 
                                        nombre=request.POST["nombre"],
                                        ced=request.POST["cedula"],
                                        sexo=request.POST["sexo"],
                                        edad=request.POST["edad"],
                                        res=request.POST["res"],)
                """

                sesion = form.save()

                id_paciente = request.POST["id_paciente"]
                sesion.id_paciente = id_paciente

                sesion = form.save()

                return redirect('/dashboard_sesiones/?id_paciente=' + id_paciente)

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

    id_paciente = request.GET["id_paciente"]
    context = {'form': form, 'id_paciente': id_paciente}
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

        upload = request.FILES['img_file']
        storage.child(str(upload)).put(upload)
        url = storage.child(str(upload)).get_url(None)
        response = requests.get(url)
        
        img = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        result = forward_single_img(img_cv)
        estimations = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

        sesion = Sesion.objects.get(pk=id_s)

        muestra = Muestra(
            sesion=sesion,
            url_img=url,
            pred=estimations[result],
        )

        muestra.save()

        return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido

    else:
        # Maneja el error de que no llegue id_paciente
        print("El request llegó vacio")
        return HttpResponse(status=400) # Problema con el request
    

def modificar_muestra(request):

    if request.POST.get("id_muestra") and request.POST.get("update"):

        id_s = request.POST["id_sesion"]
        sesion = Sesion.objects.get(pk=id_s)

        id_m = request.POST["id_muestra"]
        muestra = Muestra.objects.get(pk=id_m)

        muestra.consent = request.POST["consent"]
        muestra.is_true = request.POST["is_true"]
        muestra.obs = request.POST["obs"]

        muestra.save()

        return redirect('/dashboard_sesiones/?id_paciente=' + str(sesion.id_paciente)) # Se procesó correctamente pero no hay contenido

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

def analytics_sesion(request):

    def random_color():

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return 'rgba({}, {}, {}, 255)'.format(r,g,b)

    if request.method == "GET" and request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]

        datos_muestras = Muestra.objects.values('pred').annotate(
            cantidad=Count('pred'),
            probabilidad=Count('pred') / Count('id')).order_by('-cantidad').filter(sesion=id_s)

        data = []
        labels = []
        colors = []

        for dato in datos_muestras:
            data.append(dato['cantidad'])
            labels.append(dato['pred'])
            colors.append(random_color())
            
        data_obj = {

            'datasets' : [{
                'data' : data,
                'backgroundColor' : colors
            }],

            'labels' : labels,

        }

        data_obj = json.dumps(data_obj)

        context = {
            'datos_muestras' : datos_muestras,
            'data' : data_obj
        }

        return render(request, 'index/components/sesion_graficos.html', context)


def analytics_paciente(request):

    def random_color():

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return 'rgba({}, {}, {}, 255)'.format(r,g,b)

    if request.method == "GET" and request.GET.get("id_paciente"):

        id_p = request.GET["id_paciente"]

        sesiones = Sesion.objects.filter(id_paciente=id_p)

        datos_muestras = Muestra.objects.select_related('sesion').all()
        datos_muestras = datos_muestras.values(
            'sesion_id', 'sesion__date', 'pred', 'sesion__id_paciente').annotate(
                cantidad=Count('pred'),
                probabilidad=Count('pred') / Count('id'))
        datos_muestras = datos_muestras.order_by('-cantidad')
        datos_muestras = datos_muestras.filter(sesion__id_paciente=id_p)

        datasets = []
        labels_datasets = []

        for dato in datos_muestras:
            
            pred_existente = False
            data = []
            labels = []

            sesion_date_str = dato["sesion__date"].strftime("%d-%m-%Y")

            if sesion_date_str in labels_datasets:
                continue
            else:

                datos_muestras_fecha = datos_muestras.filter(sesion__date=dato["sesion__date"])
                data = []
                labels = []

                for dato_n in datos_muestras_fecha:
                    data.append(dato_n['cantidad'])
                    labels.append(dato_n['pred'])

                dataset = {
                    'data' : data,
                    'labels' : labels,
                    'backgroundColor': random_color()
                }

                datasets.append(dataset)
                labels_datasets.append(sesion_date_str)

        data_obj = {
            'datasets' : datasets,
            'labels' : labels_datasets
        }

        data_obj = json.dumps(data_obj)

        """
        Obtiene un resumen de los datos para graficar en tipo pie
        Esto significa que obtiene las muestras y lo único que importa es la cantidad de cada tipo
        de tumor existente en la base para el paciente.
        """

        datos_muestras = Muestra.objects.select_related('sesion').all()
        datos_muestras = datos_muestras.values('pred', 'sesion__id_paciente').annotate(
                cantidad=Count('pred'),
                probabilidad=Count('pred') / Count('id'))
        datos_muestras = datos_muestras.order_by('-cantidad')
        datos_muestras = datos_muestras.filter(sesion__id_paciente=id_p)

        data = []
        labels = []
        colors = []

        for dato in datos_muestras:
            data.append(dato['cantidad'])
            labels.append(dato['pred'])
            colors.append(random_color())

        data_pie_obj = {

            'datasets' : [{
                'data' : data,
                'backgroundColor' : colors
            }],

            'labels' : labels,

        }

        data_pie_obj = json.dumps(data_pie_obj)

        context = {
            'datos_muestras' : datos_muestras,
            'data_line' : data_obj,
            'data_pie' : data_pie_obj
        }

        return render(request, 'index/components/paciente_graficos.html', context)



def contact_us(request):
    return render(request, 'index/contact-us.html')

def features(request):
    return render(request, 'index/features.html' )
